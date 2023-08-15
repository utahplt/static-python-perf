"""Calculating (some of) the digits of pi.  This stresses big integer
arithmetic."""

"""
bg
- remove toplevel function, add `ITERATIONS` constant
- replace `timer` with `Timer`
- replaced iterators with lists
- increased NDIGITS to `5000`
"""

# import itertools
import __static__
from __static__ import int64, Array
from typing import List, Tuple

NDIGITS = 5000


# Adapted from code on http://shootout.alioth.debian.org/
def gen_x(k: int64) -> (Array[int64]):
    test: Array[int64] = Array[int64](4)
    test[0] = k
    test[1] = 4 * k + 2
    test[2] = 0
    test[3] = 2 * k + 1
    return (test)


def compose(a: Tuple[int64, int64, int64, int64], b: Tuple[int64, int64, int64, int64]) -> Tuple[
    int64, int64, int64, int64]:
    aq, ar, as_, at = a
    bq, br, bs, bt = b
    return (
        aq * bq,
        aq * br + ar * bt,
        as_ * bq + at * bs,
        as_ * br + at * bt
    )


def extract(z: Tuple[int64, int64, int64, int64], j: int64) -> int64:
    q, r, s, t = z
    q_int64: int64 = q
    r_int64: int64 = r
    s_int64: int64 = s
    t_int64: int64 = t  
    return (q_int64 * j + r_int64) // (s_int64 * j + t_int64)


def pi_digits(limit: int64) -> List[int64]:
    z = (1, 0, 0, 1)
    x = 1
    result: List[int64] = []
    while x <= limit:
        y = extract(z, 3)
        while y != extract(z, 4):
            z = compose(z, gen_x(x))
            y = extract(z, 3)
        z = compose((10, -10 * y, 0, 1), z)
        x += 1
        result.append(y)
    return result


def calc_ndigits(n: int) -> List[int64]:
    return pi_digits(n)


if __name__ == "__main__":
    result = calc_ndigits(NDIGITS)
    print(result)
