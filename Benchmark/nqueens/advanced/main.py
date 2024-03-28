"""
Simple, brute-force N-Queens solver. Using static python
Made by sebastiancr@fb.com(Sebastian Chaves) based on main.py made by collinwinter@google.com (Collin Winter)
"""
from __future__ import annotations
import __static__
from __static__ import int64, box, Array, cbool, clen
from typing import List, Generator, Iterator
import time


def static_abs(v: int64) -> int64:
    if v < 0:
        return -v
    return v


def create_array(start: int64, end: int64, step: int64) -> Array[int64]:
    """
    Function that creates an array that contains elements from start (inclusive) to end (non-inclusve) increasing the given steps
    Note: if It is not possible to go from start to end, an empty array will be returned.
    For example: create_array(2,7,2) -> (2,4,6) ; create_array(1,4,1)->(1,2,3)
    """
    c: int64 = start
    i: int64 = 0
    if (end - start) * step <= 0:
        return Array[int64](0)
    size: int64 = int64((static_abs(end - start) - 1) / static_abs(step) + 1)
    a: Array[int64] = Array[int64](box(size))
    while i < size:
        a[i] = c
        c = c + step
        i = i + 1
    return a


def permutations(pool: Array[int64], r: int64 = -1) -> Iterator[Array[int64]]:
    n = clen(pool)
    if r == -1:
        r = n
    rb = box(r)
    indices: Array[int64] = create_array(0, n, 1)
    cycles: Array[int64] = create_array(n, n - r, -1)
    per: Array[int64] = Array[int64](rb)
    idx: int64 = 0
    while idx < r:
        per[idx] = pool[indices[idx]]
        idx += 1

    yield per
    while n:
        i = rb - 1
        while i >= 0:
            cycles[i] -= 1
            if cycles[i] == 0:
                # rotate # indices[i:] = Array[int64](indices[i + 1 :] + indices[i : i + 1])
                lastN: int64 = indices[i]
                for ii in range(i + 1, len(indices)):
                    indices[ii - 1] = indices[ii]
                indices[len(indices) - 1] = lastN
                cycles[i] = n - int64(i)
            else:
                j = cycles[i]
                tmp: int64 = indices[-j]
                indices[-j] = indices[i]
                indices[i] = tmp
                idx = 0
                while idx < r:
                    per[idx] = pool[indices[idx]]
                    idx += 1
                yield per
                break
            i -= 1
        if i == -1:
            return


def solve(queen_count: int) -> Iterator[Array[int64]]:
    """N-Queens solver.

    Args:
        queen_count: the number of queens to solve for. This is also the
            board size.

    Yields:
        Solutions to the problem. Each yielded value is looks like
        (3, 8, 2, 1, 4, ..., 6) where each number is the column position for the
        queen, and the index into the tuple indicates the row.
    """

    # The generator is still needed as it is being used to check if it is a valid configuration using sets
    cols: Iterator[int] = range(queen_count)
    static_cols: Array[int64] = create_array(0, int64(queen_count), 1)
    for vec in permutations(static_cols):
        if (
                queen_count
                == len(set(vec[i] + i for i in cols))  # noqa: C401
                == len(set(vec[i] - i for i in cols))  # noqa: C401
        ):
            yield vec


def bench_n_queens(queen_count: int) -> List[Array[int64]]:
    """
    Return all the possible valid configurations of the queens
    in a board of size queen_count.
    See solve method to understand it better
    """
    return list(solve(queen_count))


if __name__ == "__main__":
    import sys

    num_iterations = 1
    if len(sys.argv) > 1:
        num_iterations = int(sys.argv[1])

    queen_count = 8
    startTime = time.time()
    for _ in range(num_iterations):
        res = bench_n_queens(queen_count)  ## main fun call?

    endTime = time.time()
    runtime = endTime - startTime
    print(runtime)

    # assert len(res) == 92
