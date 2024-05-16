import os, io
import pathlib
import click
from typing import Optional
import mypy.nodes
from mypy.parse import parse
from mypy.options import Options
from mypy.errors import CompileError, Errors


def get_files(filepath) -> list[str]:
    dir_files = []
    exclude = [".git", ".venv"]
    for root, dirs, files in os.walk(filepath, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            dir_files.append(os.path.join(root, file))

    return dir_files


def scan_file(file: str) -> Optional[int]:
    if not file.endswith(".py"):
        return
    
    f = open(pathlib.Path(file), "r", io.DEFAULT_BUFFER_SIZE)

    options = Options()
    errors = Errors(options)
    
    try:
        ast = parse(f.read(), file, None, errors, options, raise_on_error=True)
    except CompileError:
        click.echo("unable to scan file: " + file)
        return

    f.close()
    return ast