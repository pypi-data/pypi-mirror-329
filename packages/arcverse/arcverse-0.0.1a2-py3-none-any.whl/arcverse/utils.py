import numpy as np
from PIL import Image
from scipy.ndimage import label
from scipy.signal import convolve2d

# ==================== Constants ====================
COLOR_PALETTE = {
    0: {"value": 0, "name": "black", "hex": "#000000"},
    1: {"value": 1, "name": "blue", "hex": "#0074D9"},
    2: {"value": 2, "name": "red", "hex": "#FF4136"},
    3: {"value": 3, "name": "green", "hex": "#2ECC40"},
    4: {"value": 4, "name": "yellow", "hex": "#FFDC00"},
    5: {"value": 5, "name": "grey", "hex": "#AAAAAA"},
    6: {"value": 6, "name": "fuchsia", "hex": "#F012BE"},
    7: {"value": 7, "name": "orange", "hex": "#FF851B"},
    8: {"value": 8, "name": "teal", "hex": "#7FDBFF"},
    9: {"value": 9, "name": "brown", "hex": "#870C25"},
}

COLOR_LIST = list(COLOR_PALETTE.values())

SHAPE_PALETTE = {
    ".": {
        "name": ".",
        "value": np.array([[1]]),
        "type": "sym",
    },
    "..": {
        "name": "..",
        "value": np.array([[1, 1]]),
        "type": "sym",
    },
    "-": {
        "name": "-",
        "value": np.array([[1, 1, 1]]),
        "type": "sym",
    },
    "+": {
        "name": "+",
        "value": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
        "type": "sym",
    },
    "+o": {
        "name": "+o",
        "value": np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
        "type": "sym",
    },
    "sq": {
        "name": "sq",
        "value": np.array([[1, 1], [1, 1]]),
        "type": "sym",
    },
    "rt": {
        "name": "rt",
        "value": np.array([[1, 1], [1, 1], [1, 1]]),
        "type": "sym",
    },
    "tri": {
        "name": "tri",
        "value": np.array([[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]]),
        "type": "sym",
    },
    "A": {
        "name": "A",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]]),
        "type": "alpha",
    },
    "B": {
        "name": "B",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]]),
        "type": "alpha",
    },
    "c": {
        "name": "c",
        "value": np.array([[1, 1, 1], [1, 0, 1]]),
        "type": "alpha",
    },
    "C": {
        "name": "C",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 0, 1]]),
        "type": "alpha",
    },
    "D": {
        "name": "D",
        "value": np.array([[1, 1, 0], [1, 0, 1], [1, 1, 0]]),
        "type": "alpha",
    },
    "E": {
        "name": "E",
        "value": np.array([[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 1, 1]]),
        "type": "alpha",
    },
    "F": {
        "name": "F",
        "value": np.array([[1, 1, 1], [1, 0, 0], [1, 1, 0], [1, 0, 0], [1, 0, 0]]),
        "type": "alpha",
    },
    "h": {
        "name": "h",
        "value": np.array([[1, 0, 1], [1, 1, 1], [1, 0, 1]]),
        "type": "alpha",
    },
    "H": {
        "name": "H",
        "value": np.array([[1, 0, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 0, 1]]),
        "type": "alpha",
    },
    "K": {
        "name": "K",
        "value": np.array([[1, 0, 1], [1, 1, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]]),
        "type": "alpha",
    },
    "l": {
        "name": "l",
        "value": np.array([[1, 0], [1, 0], [1, 1]]),
        "type": "alpha",
    },
    "L": {
        "name": "L",
        "value": np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 1, 1]]),
        "type": "alpha",
    },
    "M": {
        "name": "M",
        "value": np.array(
            [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
            ]
        ),
        "type": "alpha",
    },
    "N": {
        "name": "N",
        "value": np.array([[1, 0, 0, 1], [1, 1, 0, 1], [1, 0, 1, 1], [1, 0, 0, 1]]),
        "type": "alpha",
    },
    "O": {
        "name": "O",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]),
        "type": "alpha",
    },
    "P": {
        "name": "P",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 0], [1, 0, 0]]),
        "type": "alpha",
    },
    "R": {
        "name": "R",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 1, 0], [1, 0, 1]]),
        "type": "alpha",
    },
    "T": {
        "name": "T",
        "value": np.array([[1, 1, 1], [0, 1, 0]]),
        "type": "alpha",
    },
    "U": {
        "name": "U",
        "value": np.array([[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]]),
        "type": "alpha",
    },
    "x": {
        "name": "x",
        "value": np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]]),
        "type": "alpha",
    },
    "y": {
        "name": "y",
        "value": np.array([[1, 0, 1], [0, 1, 0], [0, 1, 0]]),
        "type": "alpha",
    },
    "z": {
        "name": "z",
        "value": np.array([[1, 1, 0], [0, 1, 1]]),
        "type": "alpha",
    },
    "Z": {
        "name": "Z",
        "value": np.array([[1, 1, 1], [0, 1, 0], [1, 1, 1]]),
        "type": "alpha",
    },
    # S is a vflip of 2
    "0": {
        "name": "0",
        "value": np.array([[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]]),
        "type": "num",
    },
    "2": {
        "name": "2",
        "value": np.array([[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]]),
        "type": "num",
    },
    "3": {
        "name": "3",
        "value": np.array([[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]),
        "type": "num",
    },
    "4": {
        "name": "4",
        "value": np.array([[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]]),
        "type": "num",
    },
    # 5 is a vflip of 2
    "6": {
        "name": "6",
        "value": np.array([[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]]),
        "type": "num",
    },
    "7": {
        "name": "7",
        "value": np.array([[1, 1, 1], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1]]),
        "type": "num",
    },
    # 8 is the same as B
    # 9 is a v+hflip of 6
}

SHAPE_LIST = list(SHAPE_PALETTE.values())

# ==================== Utility functions ====================
# These are action functions linked to ArcWorld


# Translate function wraps numpy's roll function to shift the grid in a given direction
# by x and y units while allowing for wrap-around and no-wrap-around options
def translate(grid: np.array, x: int, y: int, wrap: bool = True) -> np.array:
    """Translate the grid by x and y units"""
    if wrap:
        return np.roll(grid, (x, y), axis=(1, 0))
    else:
        # Since numpy's roll function doesn't support no-wrap-around,
        # the array has to be manually shifted by x and y units and padded with zeros
        shifted = np.zeros_like(grid)

        x1, x2 = max(0, x), min(grid.shape[0], grid.shape[0] + x)
        y1, y2 = max(0, y), min(grid.shape[1], grid.shape[1] + y)

        x1_, x2_ = max(0, -x), min(grid.shape[0], grid.shape[0] - x)
        y1_, y2_ = max(0, -y), min(grid.shape[1], grid.shape[1] - y)

        shifted[x1:x2, y1:y2] = grid[x1_:x2_, y1_:y2_]

        return shifted


def invert(grid: np.array, fg: int) -> np.array:
    """Invert the grid"""
    # Invert the grid by flipping the foreground and background colors
    return np.where(grid > 0, 0, fg)


def detect_holes(array, connectivity=4):
    structure = (
        np.ones((3, 3), dtype=int) if connectivity == 8 else np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=int)
    )
    labeled_array, num_features = label(array == 0, structure=structure)

    holes = []
    rows, cols = array.shape

    for feature in range(1, num_features + 1):
        component = np.argwhere(labeled_array == feature)
        if all(0 < x < rows - 1 and 0 < y < cols - 1 for x, y in component):
            holes.append(component)

    return holes


# This function simply uses convolve2d to find presence/absence of a bounding box
# of a given shape in the grid
def find_open_spaces(grid: np.array, shape: np.array) -> list:
    """Find an open space in the grid for the shape"""
    # Find all the holes in the grid
    kernel = np.ones_like(shape)
    zero_mask = (grid == 0).astype(int)
    # Convolve the grid with the kernel to find all the holes
    convolved = convolve2d(zero_mask, kernel, mode="valid")
    # Get all indices where the shape can fit
    return np.argwhere(convolved == kernel.size).tolist()


# This does a brute force search for a subarray in the grid
# Using correlate
def find_subarray(grid: np.array, subarray: np.array) -> tuple | None:
    """Find the index of the subarray in the grid if it exists. Else return None"""
    windows = np.lib.stride_tricks.sliding_window_view(grid, subarray.shape)
    matches = np.all(windows == subarray, axis=(-2, -1))
    return np.argwhere(matches).tolist()


# This function is a simple clipped gaussian over integer values
def clipped_gaussian(mean: float, std: float, low: int, high: int) -> int:
    """Generate a clipped gaussian value"""
    value = int(np.random.normal(mean, std))
    return max(low, min(high, value))


# TODO: This is fully generated by copilot and I have no idea how it works
# I probably need to understand how it works or write tests to ensure it works
# as expected
def render(grid: np.ndarray, img_width: int = 200, img_height: int = 200):
    """Render the grid as an image"""
    rows, cols = grid.shape

    # Border size should be half a percent of the image width
    border_size = 1

    # Compute scale factor for the grid
    scale_width = max(1, img_width // max(1, cols))
    scale_height = max(1, img_height // max(1, rows))
    scale = min(scale_width, scale_height)

    # Convert color codes from hex to RGB
    color_rgb = np.array(
        [tuple(int(COLOR_PALETTE[i]["hex"][k : k + 2], 16) for k in (1, 3, 5)) for i in COLOR_PALETTE],
        dtype=np.uint8,
    )

    alpha = np.full((rows, cols, 1), 255, dtype=np.uint8)
    colored_grid = np.concatenate([color_rgb[grid], alpha], axis=-1)

    scaled_grid = np.kron(colored_grid, np.ones((scale, scale, 1), np.uint8))

    final_height = rows * scale + (rows - 1) * border_size
    final_width = cols * scale + (cols - 1) * border_size
    canvas = np.full((final_height, final_width, 4), (80, 80, 80, 255), dtype=np.uint8)

    row_idx = np.arange(rows * scale)
    col_idx = np.arange(cols * scale)
    row_idx += (row_idx // scale) * border_size
    col_idx += (col_idx // scale) * border_size
    canvas[row_idx[:, None], col_idx[None, :]] = scaled_grid

    return Image.fromarray(canvas, "RGBA")
