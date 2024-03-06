import __static__
from typing import List, Dict, Tuple
import time
class UnionFind:
    def __init__(self, my_dict: Dict[int, Tuple[int, int]]) -> None:
        self.my_dict = my_dict

    def add_node(self, n: int) -> None:
        self.my_dict[n] = (n, 0)

    def find(self, n: int) -> Tuple[int, int]:
        if self.my_dict[n][0] != n:
            self.my_dict[n] = self.find(self.my_dict[n][0])
        return self.my_dict[n]

    def union(self, l1: Tuple[int, int], l2: Tuple[int, int]) -> None:
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
            self.my_dict[k1] = (self.my_dict[k1][0], r1 + 1)
