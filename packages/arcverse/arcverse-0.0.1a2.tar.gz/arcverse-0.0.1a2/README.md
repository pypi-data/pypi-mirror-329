# Arcverse

---

For now, install from source:

```bash
git clone
cd arcverse
pip install -e .
```

Then, open a notebook and run:

```python
from arcverse import ArcWorld
from arcverse.utils import render

world = ArcWorld(max_rows=10, max_cols=10)
```

This will create a world that is initialized with a set of random transforms.

```python
print(world.transforms)
```

Then you can draw samples from this world as a bunch of starting grids and their corresponding transformed grids.

```python
for sample in world.sample(5):
    display(render(sample[0]))
    display(render(sample[1]))
    print("---")
```

For now, a static arc-like puzzle is created and can be accessed via:

```python
world.get_puzzle()
```

Since object shapes are random, there is a good chance all five train examples might not converge to an obvious solution but this will be refined over time.

Example
![Screenshot from 2025-02-17 00-32-13](https://github.com/user-attachments/assets/53fdaa92-8cbc-466e-b139-2053ac106b7c)
