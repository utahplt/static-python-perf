"""
Calculating (some of) the digits of pi. This stresses big integer
arithmetic.
"""
import sys
import time

"""
bg
- remove toplevel function, add `ITERATIONS` constant
- replaced iterators with lists
- increased NDIGITS to `5000`
"""

# import itertools

NDIGITS = 5000


def gen_x(k):
    return (k, 4 * k + 2, 0, 2 * k + 1)


def compose(a, b):
    aq, ar, as_, at = a
    bq, br, bs, bt = b
    return (aq * bq,
            aq * br + ar * bt,
            as_ * bq + at * bs,
            as_ * br + at * bt)


def extract(z, j):
    q, r, s, t = z
    return (q * j + r) // (s * j + t)


def pi_digits(limit):
    z = (1, 0, 0, 1)
    x = 1
    result = []
    while x <= limit:
        y = extract(z, 3)
        while y != extract(z, 4):
            z = compose(z, gen_x(x))
            y = extract(z, 3)
        z = compose((10, -10 * y, 0, 1), z)
        x += 1
        result.append(y)
    return result


def calc_ndigits(n):
    return pi_digits(n)


if __name__ == "__main__":
    # print (calc_ndigits(NDIGITS)) testing here
    start_time = time.time()
    calc_ndigits(NDIGITS)
    end_time = time.time()
    runtime = end_time - start_time
    print(runtime)
