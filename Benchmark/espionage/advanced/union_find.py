from __static__ import int64, Array, CheckedDict
from typing import Dict

class UnionFind:
    def __init__(self, my_dict: Dict[int, Array[int64]]) -> None:
        self.my_dict = CheckedDict[int, Array[int64]](my_dict)

    def add_node(self, n: int) -> None:
        arr = Array[int64](2)
        arr[0] = int64(n)
        arr[1] = 0
        self.my_dict[n] = arr

    def find(self, n: int) -> Array[int64]:
        if self.my_dict[n][0] != int64(n):
            self.my_dict[n] = self.find(self.my_dict[n][0])
        return self.my_dict[n]

    def union(self, l1: Array[int64], l2: Array[int64]) -> None:
        k1 = l1[0]
        k2 = l2[0]
        r1 = l1[1]
        r2 = l2[1]
        if r1 < r2:
            self.my_dict[k1] = l2
        elif r1 > r2:
            self.my_dict[k2] = l1
        else:
            self.my_dict[k2] = l1
            arr = Array[int64](2)
            arr[0] = self.my_dict[k1][0]
            arr[1] = r1 + 1
            self.my_dict[k1] = arr
