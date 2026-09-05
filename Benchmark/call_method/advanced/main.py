import __static__
from __static__ import int64
import time

import cinderx.jit
cinderx.jit.compile_after_n_calls(0)

"""Microbenchmark for method call overhead.

This measures simple method calls that are predictable, do not use varargs or
kwargs, and do not use tuple unpacking.

bg:
- annotated all parameters + return types
- using Timer
- removed command-line parsing
"""


class Foo(object):

    def foo(self, a: int64, b: int64, c: int64, d: int64) -> None:
        # 20 calls
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)

    def bar(self, a: int64, b: int64, c: int64) -> None:
        # 20 calls
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)

    def baz(self, a: int64, b: int64) -> None:
        # 20 calls
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)

    def quux(self, a: int64) -> None:
        # 20 calls
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()

    def qux(self) -> None:
        pass


def test_calls() -> None:
    f: Foo = Foo()
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    f.foo(1, 2, 3, 4)
    return


def main():
    startTime = time.time()
    test_calls() # call
    endTime = time.time()
    runtime = endTime - startTime
    print(runtime)
if __name__ == "__main__":
    main()
