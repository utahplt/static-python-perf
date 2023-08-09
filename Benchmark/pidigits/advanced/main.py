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
from __static__ import int64, Array, dynamic

NDIGITS = 5000


# Adapted from code on http://shootout.alioth.debian.org/
def gen_x(k: int64) -> (int64, int64, int64, int64):
    return (k, 4 * k + 2, 0, 2 * k + 1)


def compose(a: (int64, int64, int64, int64), b: (int64, int64, int64, int64)) -> (int64, int64, int64, int64):
    aq, ar, as_, at = a
    bq, br, bs, bt = b
    return (aq * bq,
            aq * br + ar * bt,
            as_ * bq + at * bs,
            as_ * br + at * bt)


def extract(z: (int64, int64, int64, int64), j: int64) -> int64:
    q, r, s, t = z
    return (q * j + r) // (s * j + t)


def pi_digits(limit: int64) -> Array[int64]:
    z = (1, 0, 0, 1)
    x = 1
    result = []
    while (x <= limit):
        y = extract(z, 3)
        while y != extract(z, 4):
            z = compose(z, gen_x(x))
            y = extract(z, 3)
        z = compose((10, -10 * y, 0, 1), z)
        x += 1
        result.append(y)
    return result


def calc_ndigits(n: int64) -> Array[int64]:
    return pi_digits(n)


if __name__ == "__main__":
    calc_ndigits(NDIGITS)
