# Copyright (c) Facebook, Inc. and its affiliates. (http://www.facebook.com)
"""
The Computer Language Benchmarks Game
http://benchmarksgame.alioth.debian.org/
Contributed by Sokolov Yura, modified by Tupteq.
"""
from __future__ import annotations

import __static__
from __static__ import box, int64, Array
from typing import Callable, List
import sys
import time

DEFAULT_ARG = 9

### SECTION SEPARATOR ###

def fannkuch(nb: int) -> int:
    n: int64 = int64(nb)
    ### SECTION SEPARATOR ###
    count: Array[int64] = Array[int64](n)
    i: int64 = 0
    while i < n:
        count[i] = i + 1
    max_flips: int64 = 0
    m: int64 = n - 1
    r: int64 = n
    ### SECTION SEPARATOR ###
    perm1: Array[int64] = Array[int64](n)
    perm: Array[int64] = Array[int64](n)
    i: int64 = 0
    while i < n:
        perm1[i] = i
        perm[i] = i
        i += 1
    perm0: Array[int64] = Array[int64](n)

    while 1:
        while r != 1:
            count[r - 1] = r
            r -= 1

        if perm1[0] != 0 and perm1[m] != m:
            i: int64 = 0
            while i < n:
                perm[i] = perm1[i]
                i += 1
            flips_count: int64 = 0
            k: int64 = perm[0]
            while k:
                i = k
                while i >= 0:
                    perm0[i] = perm[k-i]
                    i -= 1
                i = k
                while i >= 0:
                    perm[i] = perm0[i]
                    i -= 1
                flips_count += 1
                k = perm[0]

            if flips_count > max_flips:
                max_flips = flips_count

        while r != n:
            first: int64 = perm1[0]
            i = 1
            while i <= r:
                perm1[i-1] = perm1[i]
                i += 1
            perm1[r] = first
            count[r] -= 1
            if count[r] > 0:
                break
            r += 1
        else:
            return box(max_flips)
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
