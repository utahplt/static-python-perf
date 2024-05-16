import pathlib
import click
import io, os, sys
from typing import Optional
import mypy.nodes
from mypy.parse import parse
from mypy.options import Options
from mypy.errors import CompileError, Errors

sys.path.append("../helpers")
from ..helpers import get_files

def count_classes(stmt: any):
    count = 0

    if isinstance(stmt, mypy.nodes.ClassDef):
        count += 1
        for sub_stmt in stmt.defs.body:
            count += count_classes(sub_stmt)
    
    return count

def scan_file(file: str) -> Optional[int]:
    count = 0

    if not file.endswith(".py"):
        click.echo("expected .py file, got: " + file)
        return
    
    f = open(pathlib.Path(file), "r", io.DEFAULT_BUFFER_SIZE)

    options = Options()
    errors = Errors(options)
    
    try:
        ast = parse(f.read(), file, None, errors, options, raise_on_error=True)
    except CompileError:
        click.echo("unable to scan file: " + file)
        return

    for stmt in ast.defs:
        count += count_classes(stmt)

    f.close()
    return count

@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def count(filepath) -> None:
    res = {}
    
    if os.path.isdir(filepath):
        dir_files = get_files(filepath)

        for file in dir_files:
            count = scan_file(file)

            res[file] = count
        
    else:
        count = scan_file(file)
        res[file] = count

    print(res)

if __name__ == "__main__":
    count()