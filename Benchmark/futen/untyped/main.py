from os import path
from futen import get_netlocs, execute

def main(n):
    testfile = path.join(path.dirname(__file__), '../ssh.config.dat')
    expect = {'web': '2200', 'app': '2201', 'db': '2202'}
    with open(testfile) as fd:
        lines = fd.readlines()
        actual = None
        for i in range(n):
            actual = get_netlocs(lines, dict)  # Pass dict as an argument
        if expect != actual:
            raise AssertionError("'%s' is not equal to '%s'" % (expect, actual))

    testfile = path.join(path.dirname(__file__), '../ssh.config.dat')
    template = path.join(path.dirname(__file__), '../inventory_template.dat')
    expectfile = path.join(path.dirname(__file__), 'inventory_expect.dat')
    with open(expectfile) as fd:
        expect = ''.join(fd.readlines()).strip()
    with open(testfile) as fd:
        lines = fd.readlines()
        result = None
        for i in range(n):
            result = execute(lines, template)
        if result != expect:
            raise ValueError("'%s' is not equal to '%s'" % (expect, result))
    return

main(1900)
