import pathlib
import click
import io, os, sys
from typing import Optional
import mypy.nodes
from mypy.parse import parse
from mypy.options import Options
from mypy.errors import CompileError, Errors
import pprint

sys.path.append("../helpers")
from helpers import get_files, scan_file

def count_classes(stmt: any):
    count = 0

    if isinstance(stmt, mypy.nodes.ClassDef):
        count += 1
        for sub_stmt in stmt.defs.body:
            count += count_classes(sub_stmt)
    
    return count

@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def count(filepath) -> None:
    res = {}
    
    if os.path.isdir(filepath):
        dir_files = get_files(filepath)

        for file in dir_files:
            count = 0
            ast = scan_file(file)

            if ast is not None:
                for stmt in ast.defs:
                    count += count_classes(stmt)

                res[file] = count
        
    else:
        ast = scan_file(filepath)

        if ast is not None:
            for stmt in ast.defs:
                count += count_classes(stmt)

            res[filepath] = count

    pprint.pp(res)

# todo: take multiple files?
if __name__ == "__main__":
    count()