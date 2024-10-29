# Copyright (c) Facebook, Inc. and its affiliates. (http://www.facebook.com)
"""
The Computer Language Benchmarks Game
http://benchmarksgame.alioth.debian.org/
Contributed by Sokolov Yura, modified by Tupteq.
"""
from __future__ import annotations

import __static__
import sys
from typing import Callable, List
import time

DEFAULT_ARG = 9

### SECTION SEPARATOR ###

def fannkuch(n: int) -> int:
    ### SECTION SEPARATOR ###
    count: List[int] = list(range(1, n + 1))
    max_flips: int = 0
    m: int = n - 1
    r: int = n
    ### SECTION SEPARATOR ###
    perm1: List[int] = list(range(n))
    perm: List[int] = list(range(n))
    perm1_ins: Callable[[int, int], None] = perm1.insert
    perm1_pop: Callable[[int], int] = perm1.pop
    ### SHALLOW SEPARATOR ###

    while 1:
        while r != 1:
            count[r - 1] = r
            r -= 1

        ### SHALLOW SEPARATOR ###
        if perm1[0] != 0 and perm1[m] != m:
            perm = perm1[:]
            flips_count: int = 0
            k: int = perm[0]
            ### SHALLOW SEPARATOR ###
            while k:
                perm[: k + 1] = perm[k::-1]
                flips_count += 1
                k = perm[0]

            if flips_count > max_flips:
                max_flips = flips_count

        while r != n:
            perm1_ins(r, perm1_pop(0))
            count[r] -= 1
            if count[r] > 0:
                break
            r += 1
        else:
            return max_flips
    return 0

### SECTION SEPARATOR ###

if __name__ == "__main__":
    num_iterations = 1
    if len(sys.argv) > 1:
        num_iterations = int(sys.argv[1])

    start_time = time.time()
    for _ in range(num_iterations):
        res = fannkuch(DEFAULT_ARG)
        assert res == 30
    end_time = time.time()
    runtime = end_time - start_time
    print(runtime / num_iterations)
