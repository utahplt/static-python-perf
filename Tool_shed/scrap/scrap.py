import click
import sys

sys.path.append("../helpers")
from helpers import get_files, scan_file

@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def scrap(filepath) -> None:
    ...

if __name__ == "__main__":
    scrap()