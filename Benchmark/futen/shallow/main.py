from os import path
from futen import get_netlocs, execute
import __static__
import time
def main(n: int) -> None:
    testfile = '../ssh.config.dat'
    expect = {'web': '2200', 'app': '2201', 'db': '2202'}
    with open(testfile) as fd:
        lines = fd.readlines()
        actual = None
        for i in range(n):
            actual = get_netlocs(lines)
        if expect != actual:
            raise AssertionError("'%s' is not equal to '%s'" % (expect, actual))

    testfile = '../ssh.config.dat'
    template = '../inventory_template.dat'
    expectfile = 'inventory_expect.dat'
    with open(expectfile) as fd:
        expect = ''.join(fd.readlines()).strip()
    with open(testfile) as fd:
        lines = fd.readlines()
        result = None
        for i in range(n):
            result = execute(lines, template)
        if result != expect:
            raise ValueError("'%s' is not equal to '%s'" % (expect, result))

start = time.time()
main(1900)
endTime = time.time()
runtime = endTime - start
print(runtime)
