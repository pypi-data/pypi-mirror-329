"""Command-line interface."""

import click
from config import DATA_DIR


@click.command()
@click.version_option()
def main() -> None:
    with open(DATA_DIR / "hello.txt", "w") as f:
        f.write("Hello, world!")
    click.echo(f"See the output in the data directory: {DATA_DIR}")


if __name__ == "__main__":
    main()  # pragma: no cover
