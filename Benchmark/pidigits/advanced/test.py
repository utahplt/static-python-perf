import __static__
from __static__ import int64, Array

def gen_x(k: int64) -> (Array[int64]):
    test: Array[int64] = Array[int64](4)
    test[0] = k
    test[1] = 4 * k + 2
    test[2] = 0
    test[3] = 2 * k + 1
    return (test)