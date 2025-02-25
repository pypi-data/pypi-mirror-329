import random
from functools import partial
from typing import Any, Dict, List

import numpy as np
from loguru import logger

from .utils import (
    COLOR_LIST,
    SHAPE_LIST,
    clipped_gaussian,
    detect_holes,
    find_open_spaces,
    find_subarray,
    invert,
    render,
    translate,
)


# Things are structures in the arc-world made up of simpler shapes & colors
# Simplest things are monochromatic basic shapes
# Complex things combine multiple basic shapes and colors
# Each thing, after construction computes secondary attributes like area, size, etc.
class GridThing:
    def __init__(
        self,
        shapes: List[Dict[str, Any]] | None = None,
        colors: List[Dict[str, Any]] | None = None,
        num_shapes: int = 1,
        num_colors: int = 1,
        debug: bool = False,
    ):
        # Shapes & colors can be passed in or default to the global lists
        shapes = shapes if shapes is not None else SHAPE_LIST
        # Colors are always foreground colors and the first color (black) is reserved for background
        colors = colors if colors is not None else COLOR_LIST[1:]

        # Ensure that the number of samples don't exceed the number of available shapes and colors
        self.num_shapes = min(num_shapes, len(shapes))
        self.num_colors = min(num_colors, len(colors))

        # Now select a random number of candidate shapes & colors
        self._selected_shapes = random.sample(shapes, self.num_shapes)
        self._selected_colors = random.sample(colors, self.num_colors)
        self.debug = debug

        # Log the selected shapes and colors if debug is enabled
        if self.debug:
            logger.info(f"Creating a thing with {self.num_shapes} shapes and {self.num_colors} colors")
            logger.info(f"Selected shapes: {[shape['name'] for shape in self._selected_shapes]}")
            logger.info(f"Selected colors: {[color['name'] for color in self._selected_colors]}")

        # Create the structure
        self.grid = self._make_thing()

        # Compute thing attributes that are typically used as action params in the arc-world
        self._populate_attributes()

    # This creates a random structure by taking a random sample of shapes and colors
    # Each structure is meant to operate cohesive as a single entity in the GridWorld
    def _make_thing(self):
        # Now, for each shape, assign a random color and apply a random transformation
        pieces = []
        for selected_shape in self._selected_shapes:
            # Apply one of identity, flip, rotate, or tile transforms with weighted probabilities
            transform = random.choices(
                [
                    # Identity returns the grid as is
                    lambda x: x,
                    # Rest are partial functions
                    partial(np.flip, axis=random.choice([0, 1])),
                    partial(np.rot90, k=random.randint(1, 3)),
                    np.transpose,
                    partial(np.tile, reps=(random.randint(1, 2), random.randint(1, 2))),
                ],
                weights=[0.25, 0.25, 0.25, 0.20, 0.05],
                k=1,
            )[0]

            # Apply a random transformation to the shape
            if self.debug:
                logger.info(f"Applying transformation to shape {selected_shape['name']}")
            piece = transform(selected_shape["value"])
            if self.debug:
                logger.info(f"Shape {selected_shape['name']} transformed to {piece}")
            # Assign a random color to the shape
            color = random.choice(self._selected_colors)
            if self.debug:
                logger.info(f"Assigning color {color['name']} to shape {selected_shape['name']}")
            # Since color is simply captured by the value of the shape, multiply it
            piece = np.multiply(piece, color["value"])
            # Gather the pieces
            pieces.append(piece)

        if self.debug:
            logger.info(f"Shapes combined: {pieces}")

        # Each piece can be of different size, so randomly put them together so that
        # the yield if the smallest possible grid that can contain all the pieces
        # First, pick the largest shape by total number of cells
        # Then remove it from the list of pieces
        random.shuffle(pieces)
        structure = pieces.pop(0)

        # For the remaining pieces, randomly add them to the structure
        for piece in pieces:
            # First create a zeros canvas of the same size as the largest shape
            canvas = np.zeros(
                (max(structure.shape[0], piece.shape[0]), max(structure.shape[1], piece.shape[1])),
                dtype=int,
            )

            # Place structure on a random corner of the canvas
            start_row = random.choice([0, canvas.shape[0] - structure.shape[0]])
            start_col = random.choice([0, canvas.shape[1] - structure.shape[1]])
            canvas[start_row : start_row + structure.shape[0], start_col : start_col + structure.shape[1]] = structure

            # Next, randomly place the piece on the canvas
            start_row = random.randint(0, canvas.shape[0] - piece.shape[0])
            start_col = random.randint(0, canvas.shape[1] - piece.shape[1])
            canvas[start_row : start_row + piece.shape[0], start_col : start_col + piece.shape[1]] = piece

            # Update the structure
            structure = canvas

            # Trim the structure to remove any zero rows or columns
            structure = np.trim_zeros(structure)

            if self.debug:
                logger.info(f"Structure after attaching shape - {structure}")

        if self.debug:
            logger.info(f"Final structure: {structure}")

        return structure

    def _populate_attributes(self):
        # Get basic attributes about the structure
        self.height, self.width = self.grid.shape
        # Count number of on and off cells
        self.size = np.count_nonzero(self.grid)
        self.area = self.height * self.width
        # Compute fill as the ratio of on cells to total cells
        self.fill = self.size / self.area
        # Compute number of unique colors and their counts
        self.colors = {}
        for color, count in zip(*np.unique(self.grid, return_counts=True)):
            if color != 0:
                self.colors[color] = count

        # Primary color is the color with the maximum count and is simply called color
        self.primary_color = max(self.colors, key=self.colors.get)
        self.primary_color_count = self.colors[self.primary_color]

        # Compute the number of holes - areas of 0s surrounded by 1s
        holes4_xy = detect_holes(self.grid, connectivity=4)
        self.num_part_holes = len(holes4_xy)
        self.part_holes = np.zeros_like(self.grid)
        for hole in holes4_xy:
            self.part_holes[hole[:, 0], hole[:, 1]] = 1

        holes8_xy = detect_holes(self.grid, connectivity=8)
        self.num_full_holes = len(holes8_xy)
        self.full_holes = np.zeros_like(self.grid)
        for hole in holes8_xy:
            self.full_holes[hole[:, 0], hole[:, 1]] = 1

        self.part_holes_area = np.count_nonzero(self.part_holes)
        self.full_holes_area = np.count_nonzero(self.full_holes)

        # TODO: Add more attributes that humans easily recognize in spatial structures

    def render(self, img_width: int = 200, img_height: int = 200):
        return render(self.grid, img_width, img_height)


class GridRule:
    """Rule represents a transformation that can be applied to a grid or a thing in the world"""

    def __init__(
        self,
        scope: str = "thing",
        complexity: int = 0.01,
        wrap_prob: float = 0.1,
        translate_max_x: int = 4,
        translate_max_y: int = 4,
        debug: bool = False,
    ):
        self.scope = scope
        self.complexity = complexity
        self.wrap = random.random() < wrap_prob
        # Initialize object with random param values for all the possible transformations in arcverse
        self.translate_x = clipped_gaussian(0, translate_max_x // 2, -translate_max_x, translate_max_x)
        self.translate_y = clipped_gaussian(0, translate_max_y // 2, -translate_max_y, translate_max_y)
        self.flip_axis = random.choice([0, 1])
        self.rotate_k = min(np.random.geometric(0.5), 3)
        self.tile_reps = (random.randint(1, 2), random.randint(1, 2))
        self.invert_fg = random.randint(1, 9)
        self.debug = debug

        # Create a pool of rules to draw from
        self._rules = [
            {"name": "translate", "weight": 10, "scope": ["thing"]},
            {"name": "flip", "weight": 4, "scope": ["thing", "grid"]},
            {"name": "rotate", "weight": 4, "scope": ["thing", "grid"]},
            # {"name": "tile", "weight": 1, "scope": ["thing"]},
            # {"name": "trim_zeros", "weight": 1, "scope": ["grid"]},
            {"name": "invert", "weight": 1, "scope": ["grid"]},
            # TODO: Add color and other complex transformations beyond simple geometric transformations
        ]

        # Create ruleset as applicable functions
        self.ruleset = self._make_rules()

    def _make_rules(self):
        """This function creates a set of rules based on the complexity and scope of the rule"""
        # First filter the rules based on the scope
        rules = [rule for rule in self._rules if self.scope in rule["scope"]]
        # Normalize the weights and round probabilities to 2 decimal places
        # To ensure they sum to 1, make the last probability 1 - sum of all previous probabilities
        total_weight = sum([t["weight"] for t in rules])
        for rule in rules[:-1]:
            rule["probability"] = round(rule["weight"] / total_weight, 2)
        rules[-1]["probability"] = 1 - sum([t["probability"] for t in rules[:-1]])

        # Number of rules should exponentially decrease
        num_rules = min(np.random.geometric(1 - self.complexity), len(rules))

        selected_rules = np.random.choice(rules, num_rules, replace=False, p=[rule["probability"] for rule in rules])

        return set([rule["name"] for rule in selected_rules])

    def apply(self, grid: np.array, thing: np.array, start_row: int, start_col: int, step: int = 0):
        """This function applies the rule to the grid or thing based on the scope of the rule"""
        # Apply the rules to the grid or thing based on the scope
        curr_row = start_row
        curr_col = start_col
        curr_thing = np.copy(thing)

        for _ in range(step):
            if "flip" in self.ruleset:
                curr_thing = np.flip(curr_thing, axis=self.flip_axis)
            if "rotate" in self.ruleset:
                curr_thing = np.rot90(curr_thing, k=self.rotate_k)
            if "trim_zeros" in self.ruleset:
                curr_thing = np.trim_zeros(curr_thing)
            if "invert" in self.ruleset:
                curr_thing = invert(curr_thing, fg=self.invert_fg)
            if "tile" in self.ruleset:
                curr_thing = np.tile(curr_thing, reps=self.tile_reps)
            if "translate" in self.ruleset:
                curr_row, curr_col = curr_row + self.translate_x, curr_col + self.translate_y

        new_grid = self._update_grid(grid, curr_thing, curr_row, curr_col)

        if self.debug:
            logger.info(f"Grid updated with rule {self.ruleset} at step {step}: {new_grid}")

        return new_grid

    def _update_grid(self, grid: np.array, thing: np.array, start_row: int, start_col: int) -> np.array:
        # Create a copy of the grid to avoid modifying the original
        layer = np.zeros_like(grid)
        # Simply place the thing at (0, 0) and then translate it to the start row and column with wrap/no-wrap
        layer[: thing.shape[0], : thing.shape[1]] = thing
        # Translate the thing to the start row and column
        layer = translate(layer, start_row, start_col, wrap=self.wrap)

        # Update the copy with non-zero elements from the layer
        new_grid = np.copy(grid)
        new_grid[layer != 0] = layer[layer != 0]

        return new_grid


class GridState:
    """State represents a snapshot of the world from a particular perspective at a particular time.
    It can also generate subsequent states by applying rules (transformations) to the current state.
    The state is identified by a specific grid size and a subset of things in the world with relative positions.
    """

    def __init__(
        self,
        grouped_things: List[Dict[str, Any]],
        border: int = 1,
        debug: bool = False,
    ):
        """
        Initialize the GridState.

        Parameters:
        grouped_things (List[Dict[str, Any]]): List of grouped things.
        border (int): Border size around each thing. Default is 1.
        debug (bool): Enable debug logging. Default is False.
        """
        self.grouped_things = grouped_things
        self.border = border
        self.debug = debug

        # Initialize the grid based on things
        self.canvas = self._init_grid()

        # Set grid sizes for the state
        self.num_rows, self.num_cols = self.canvas.shape

        # Create a list of layers with things and their positions
        self.layers = self._create_layers(self.canvas, self.grouped_things)

    def _init_grid(self):
        """This function initializes the grid by randomly placing things in it"""
        # Randomly grab things and iteratively expand the canvas as needed
        # to accommodate all the things and then add random sided paddings

        # First yank out all the things from different groups
        all_things = [thing for group in self.grouped_things for thing in group["things"]]

        # Randomly shuffle the things
        random.shuffle(all_things)

        # Now initiate the canvas with the first thing's grid values
        canvas = all_things.pop(0).grid

        if self.debug:
            logger.info(f"Canvas initiated with the first thing: {canvas}")

        # For the remaining things, randomly add them while preventing overlap
        for thing in all_things:
            # Grab the thing's grid and add a border around it to create separation if needed
            thing_canvas = np.pad(thing.grid, self.border, mode="constant")

            if self.debug:
                logger.info(f"Placing thing {thing_canvas}")

            # First try to find valid open spaces for the thing
            # If canvas & thing are different across rows and columns, this will error out so handle it
            try:
                open_spaces = find_open_spaces(canvas, thing_canvas)
            except ValueError:
                open_spaces = []

            if self.debug:
                logger.info(f"{len(open_spaces)} open spaces found for thing {thing}")

            # If there are no open spaces, this simply means that it is either the first thing
            # or the current canvas is too small to accommodate the thing
            if not open_spaces:
                # First create a new canvas of the same size as the sum of the current canvas and the thing
                new_canvas = np.zeros(
                    (canvas.shape[0] + thing_canvas.shape[0], canvas.shape[1] + thing_canvas.shape[1]),
                    dtype=int,
                )

                # Place the current canvas on a random corner of the new canvas
                start_row = random.choice([0, new_canvas.shape[0] - canvas.shape[0]])
                start_col = random.choice([0, new_canvas.shape[1] - canvas.shape[1]])
                new_canvas[start_row : start_row + canvas.shape[0], start_col : start_col + canvas.shape[1]] = canvas

                # Update the canvas with the new canvas
                canvas = new_canvas

                # Next get valid starting spaces for the thing and randomly select one
                open_spaces = find_open_spaces(canvas, thing_canvas)
                if self.debug:
                    logger.info(f"{len(open_spaces)} open spaces found for thing {thing} on new canvas")

            # Now randomly select a valid open space for the thing
            start_row, start_col = random.choice(open_spaces)

            # Place the thing on the canvas
            canvas[
                start_row : start_row + thing_canvas.shape[0],
                start_col : start_col + thing_canvas.shape[1],
            ] = thing_canvas

            if self.debug:
                logger.info(f"Thing {thing} placed at ({start_row}, {start_col})")

        # Now trim all zeros and randomly pad the canvas
        canvas = np.trim_zeros(canvas)

        pad_top = clipped_gaussian(3, 2, 1, 6)
        pad_bottom = clipped_gaussian(3, 2, 1, 6)
        pad_left = clipped_gaussian(3, 2, 1, 6)
        pad_right = clipped_gaussian(3, 2, 1, 6)
        canvas = np.pad(canvas, ((pad_top, pad_bottom), (pad_left, pad_right)), mode="constant")

        if self.debug:
            logger.info(f"Canvas after padding: {canvas}")

        return canvas

    def _create_layers(self, canvas: np.array, grouped_things: List[Dict[str, Any]]):
        """This function initializes the layers with things and their positions in the grid"""

        # For each thing, create a layer in the grid with its position & rules
        layers = []

        for grouped_thing in grouped_things:
            if self.debug:
                logger.info(f"Group: {grouped_thing}")
            # For each thing, create a layer with its position & rules
            for thing in grouped_thing["things"]:
                if self.debug:
                    logger.info(f"Thing: {thing}")
                # Find the position of the thing in the canvas
                matches = find_subarray(canvas, thing.grid)
                if not matches:
                    raise ValueError(f"Thing {thing} not found in the canvas")
                else:
                    start_row, start_col = matches[0]

                layers.append(
                    {
                        "thing": thing,
                        "rules": grouped_thing["rules"],
                        "start_row": start_row,
                        "start_col": start_col,
                    }
                )

        if self.debug:
            logger.info(f"Layers: {layers}")

        return layers

    def get_grid(self, step: int = 0) -> np.array:
        # This function will return the grid at a particular step
        # by iteratively applying the rules to the grid starting from the initial grid
        # and updating the grid at each step
        grid = np.zeros((self.num_rows, self.num_cols), dtype=int)
        for layer in self.layers:
            rules = layer["rules"]
            grid = rules.apply(grid, layer["thing"].grid, layer["start_row"], layer["start_col"], step)

        if self.debug:
            logger.info(f"Grid at step {step}: {grid}")

        return grid

    # This function updates the grid by overriding the non-zero elements from the layer
    # on top of the existing grid
    def _update_grid(self, grid: np.array, layer: np.array) -> np.array:
        # Create a copy of the grid to avoid modifying the original
        new_grid = np.copy(grid)
        # Update the copy with non-zero elements from the layer
        new_grid[layer != 0] = layer[layer != 0]
        return new_grid

    def render(self, step: int = 0, img_width: int = 200, img_height: int = 200):
        return render(self.get_grid(step), img_width, img_height)


class GridWorld:
    """GridWorld represent a world in the arcverse that is populated with a set of things
    governed by a set of universal & class-specific rules.
    """

    def __init__(
        self,
        level: int = 1,
        min_rows: int = 5,
        min_cols: int = 5,
        max_rows: int = 50,
        max_cols: int = 50,
        num_things: int = 100,
        monochrome: bool = True,
        wrap_prob: float = 0.1,
        color_complexity: float = 0.01,
        shape_complexity: float = 0.01,
        thing_complexity: float = 0.01,
        rule_complexity: float = 0.01,
        debug: bool = False,
    ):
        # Levels are used to determine the complexity of the world
        self.level = level
        self.debug = debug
        # Bounds for any grid in this world
        self.min_rows = min_rows
        self.min_cols = min_cols
        self.max_rows = max_rows
        self.max_cols = max_cols
        # Number of things in the world
        self.num_things = num_things

        self.monochrome = monochrome
        self.wrap_prob = wrap_prob
        # Simplicity params dictate how complex things are and how many rules are applied
        self.shape_complexity = shape_complexity
        self.color_complexity = color_complexity
        self.thing_complexity = thing_complexity
        self.rule_complexity = rule_complexity

        # Populate the world with things
        self.grouped_things = self._make_things()

        # Next, add a series of per-class transformations
        self._make_rules()

    def _make_things(self):
        """This is the primary function that populates the world with different classes of things
        that can be transformed in different ways"""

        filter_features = {
            "primary_color": [color["value"] for color in COLOR_LIST[1:]],
            "height": list(range(3, 5)),
            "width": list(range(3, 5)),
            "size": list([5, 10, 15, 20, 25]),
            "fill": list([0.1, 0.5, 0.9]),
            "holes": list([0, 1, 2, 3]),
        }

        # Randomly create a set of things with varying shapes, sizes and colors
        things = []
        for _ in range(self.num_things):
            num_shapes = min(np.random.geometric(1 - self.shape_complexity), 9)
            num_colors = min(np.random.geometric(1 - self.color_complexity), 9) if not self.monochrome else 1
            if self.debug:
                logger.info(f"Creating a thing with {num_shapes} shapes and {num_colors} colors ")
            thing = GridThing(num_shapes=num_shapes, num_colors=num_colors, debug=self.debug)
            things.append(thing)

        # At the lowest level, there are no things and all rules are applied to the entire grid
        # Grids are simply filled with random shapes and colors with no structure
        if self.level == 0:
            pass

        # At level 1, things are created with random shapes, colors and sizes
        # and all transformations are applied per-thing
        if self.level == 1:
            # By default, all things are at the base level of abstraction
            # This means that transformations are applied to the entire grid
            groups = [
                {
                    "level": 1,
                    "group": 1,
                    "name": "all",
                    "description": "All transformations are on the entire grid",
                    "things": things,
                }
            ]

        # Next, if level is 2, this would mean that things are split into two groups
        # with exactly one feature as the distinguishing factor
        # For instance, primary color or size etc.
        # Right now this is hardcoded - in the near future, this will be more flexible to include arbitrary
        # features, their values and combinations with and-or conditions
        if self.level == 2:
            # Pick a random feature
            # feature = random.choice(list(filter_features.keys()))
            # For now only use color
            feature = "primary_color"
            feature_value = random.choice(filter_features[feature])

            # Split the things into two groups based on the feature
            in_group = {"level": 2, "group": 1, "name": f"{feature}_{feature_value}", "things": []}
            out_group = {"level": 2, "group": 2, "name": f"not_{feature}_{feature_value}", "things": []}

            for thing in things:
                if thing.__dict__[feature] == feature_value:
                    in_group["things"].append(thing)
                else:
                    out_group["things"].append(thing)

            groups = [in_group, out_group]

        return groups

    def _make_rules(self):
        """Creates rules as a series of transforms applied to different classes of things in the world"""
        # Go over each level and create rules for each class of things
        for group in self.grouped_things:
            # Randomly select rules
            group["rules"] = GridRule(complexity=self.rule_complexity, wrap_prob=self.wrap_prob, debug=self.debug)

    def get_samples(self, n: int = 2):
        """This function generates n samples of the world by applying the transformations to the grid"""
        # NOTE: All group + tranformations must be covered by the sample even if an individual on might not
        # For now, every sample will cover all groups and transformations but this will be relaxed in the future
        samples = []
        for _ in range(n):
            # Sample an arbitrary number of things from each group
            sample_things = []
            for group in self.grouped_things:
                num_things = min(np.random.geometric(1 - self.thing_complexity), 3)
                selected_things = random.sample(group["things"], num_things)
                # Next, attach the rules to the selected things as a tuple
                sample_things.append(
                    {
                        "name": group["name"],
                        "group": group["group"],
                        "level": group["level"],
                        "things": selected_things,
                        "rules": group["rules"],
                    }
                )
            if self.debug:
                logger.info(f"Sample things: {sample_things}")

            # Now, create a grid state with the sample things
            sample_grid = GridState(sample_things, debug=self.debug)

            samples.append(sample_grid)

        return samples

    # def _create_puzzle(self):
    #     # Create 5 training examples and one test example and save it in arc-puzzle format
    #     puzzle = {"train": [], "test": []}

    #     train_samples = self.sample(5)

    #     for sample in train_samples:
    #         puzzle["train"].append({"input": sample[0].tolist(), "output": sample[1].tolist()})

    #     test_sample = self.sample(2)

    #     for sample in test_sample:
    #         puzzle["test"].append({"input": sample[0].tolist(), "output": sample[1].tolist()})

    #     return puzzle

    # def get_puzzle(self):
    #     return self.puzzle

    @property
    def min_rows(self):
        return self._min_rows

    @min_rows.setter
    def min_rows(self, value):
        if value < 5:
            raise ValueError("min_rows must be at least 5")
        self._min_rows = value

    @property
    def min_cols(self):
        return self._min_cols

    @min_cols.setter
    def min_cols(self, value):
        if value < 5:
            raise ValueError("min_cols must be at least 5")
        self._min_cols = value

    @property
    def max_rows(self):
        return self._max_rows

    @max_rows.setter
    def max_rows(self, value):
        if value <= self.min_rows or value > 50:
            raise ValueError("max_rows must be greater than min_rows and less than or equal to 30")
        self._max_rows = value

    @property
    def max_cols(self):
        return self._max_cols

    @max_cols.setter
    def max_cols(self, value):
        if value <= self.min_cols or value > 50:
            raise ValueError("max_cols must be greater than min_cols and less than or equal to 30")
        self._max_cols = value

    # Complexity values should be between 0.01 and 0.99
    @property
    def thing_complexity(self):
        return self._thing_complexity

    @thing_complexity.setter
    def thing_complexity(self, value):
        if value < 0.01:
            logger.warning("thing_complexity capped to 0.01")
            value = 0.01
        elif value > 0.99:
            logger.warning("thing_complexity capped to 0.99")
            value = 0.99
        self._thing_complexity = value

    @property
    def rule_complexity(self):
        return self._rule_complexity

    @rule_complexity.setter
    def rule_complexity(self, value):
        if value < 0.01:
            logger.warning("rule_complexity capped to 0.01")
            value = 0.01
        elif value > 0.99:
            logger.warning("rule_complexity capped to 0.99")
            value = 0.99
        self._rule_complexity = value

    @property
    def shape_complexity(self):
        return self._shape_complexity

    @shape_complexity.setter
    def shape_complexity(self, value):
        if value < 0.01:
            logger.warning("shape_complexity capped to 0.01")
            value = 0.01
        elif value > 0.99:
            logger.warning("shape_complexity capped to 0.99")
            value = 0.99
        self._shape_complexity = value

    @property
    def color_complexity(self):
        return self._color_complexity

    @color_complexity.setter
    def color_complexity(self, value):
        if value < 0.01:
            logger.warning("color_complexity capped to 0.01")
            value = 0.01
        elif value > 0.99:
            logger.warning("color_complexity capped to 0.99")
            value = 0.99
        self._color_complexity = value

    def __repr__(self):
        return (
            f"GridWorld(num_things={self.num_things}, min_rows={self.min_rows}, "
            f"min_cols={self.min_cols}, max_rows={self.max_rows}, max_cols={self.max_cols})"
        )

    def __str__(self):
        return (
            f"GridWorld: {self.num_things} things, {self.min_rows}x{self.min_cols} "
            f"to {self.max_rows}x{self.max_cols}"
        )
