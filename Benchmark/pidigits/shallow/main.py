from __future__ import annotations
import __static__
from typing import List, Tuple
import time
"""
Calculating (some of) the digits of pi. This stresses big integer
arithmetic.
"""

"""
bg
- remove toplevel function, add `ITERATIONS` constant
- replaced iterators with lists
- increased NDIGITS to `5000`
"""

NDIGITS: int = 5000


# Adapted from code on http://shootout.alioth.debian.org/
def gen_x(k: int) -> Tuple[int, int, int, int]:
    return (k, 4 * k + 2, 0, 2 * k + 1)


def compose(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    aq, ar, as_, at = a
    bq, br, bs, bt = b
    return (aq * bq,
            aq * br + ar * bt,
            as_ * bq + at * bs,
            as_ * br + at * bt)


def extract(z: Tuple[int, int, int, int], j: int) -> int:
    q, r, s, t = z
    return (q * j + r) // (s * j + t)


def pi_digits(limit: int) -> List[int]:
    z = (1, 0, 0, 1)
    x = 1
    result: List[int] = []
    while x <= limit:
        y = extract(z, 3)
        while y != extract(z, 4):
            z = compose(z, gen_x(x))
            y = extract(z, 3)
        z = compose((10, -10 * y, 0, 1), z)
        x += 1
        result.append(y)
    return result


def calc_ndigits(n: int) -> List[int]:
    return pi_digits(n)


if __name__ == "__main__":

    startTime = time.time()
    calc_ndigits(NDIGITS)
    endTime = time.time()
    runtime = endTime - startTime
    print(runtime)
