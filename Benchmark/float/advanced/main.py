"""
bg:
- add `ITERATIONS` constant
- remove `main` function
- add missing type annotations
- replace `xrange` with `range`
- remove unused imports
"""
from __future__ import annotations
import __static__
from __static__ import int64, float64
from math import sin, cos, sqrt
from typing import List

class Point(object):
    def __init__(self, i: float64) -> None:
        self.x = x = sin(i)
        self.y = cos(i) * 3
        self.z = (x * x) / 2

    def normalize(self) -> None:
        x = self.x
        y = self.y
        z = self.z
        norm = sqrt(x * x + y * y + z * z)
        self.x /= norm
        self.y /= norm
        self.z /= norm

    def maximize(self, other: Point) -> Point:
        self.x = self.x if self.x > other.x else other.x
        self.y = self.y if self.y > other.y else other.y
        self.z = self.z if self.z > other.z else other.z
        return self

def maximize(points: List[Point]) -> Point:
    next_point = points[0]
    for p in points[1:]:
        next_point = next_point.maximize(p)
    return next_point

def benchmark(n: int64) -> Point:
    points = [Point(i) for i in range(n)]
    for p in points:
        p.normalize()
    return maximize(points)

POINTS = 200000

if __name__ == "__main__":
    benchmark(POINTS)
