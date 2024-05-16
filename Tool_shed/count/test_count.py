from mypy.parse import parse
from mypy.options import Options
from mypy.errors import Errors

from count import count_classes

basic_class = r'''
class Basic():
    pass
'''

nested_class = r'''
class Basic():
    x: int = 0
    
    class Nested():
        y = 0
'''

def parse_str(stub: str) -> tuple[any, str]:

    options = Options()
    errors = Errors(options)

    # ast = parse(stub, 'test', None, errors, options, raise_on_error=True)
    ast = parse(stub, 'test', None, errors, options)

    if 'test' not in errors.error_info_map:
        return ast, ''
    else:
        return ast, errors.error_info_map['test'][0].message

def check_err(err: str) -> None:
    if err != '':
        print(err)

def test_basic_class():
    ast, err = parse_str(basic_class)
    check_err(err)

    count = 0

    for stmt in ast.defs:
        count += count_classes(stmt)

    assert count == 1

def test_nested_class():
    ast, err = parse_str(nested_class)
    check_err(err)

    count = 0

    for stmt in ast.defs:
        count += count_classes(stmt)

    assert count == 2


if __name__ == "__main__":
    ...