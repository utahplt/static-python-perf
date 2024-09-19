from __future__ import annotations
from math import sin, cos, sqrt
from __static__ import CheckedList, inline
from typing import final
import time
"""
bg:
- add `ITERATIONS` constant
- remove `main` function
- add missing type annotations
- replace `xrange` with `range`
- remove unused imports
"""

@final
class Point(object):

    def __init__(self: Point, i: float) -> None:
        x: float = sin(i)  # does this not have to be a float?
        self.x: float = x
        self.y: float = cos(i) * 3
        self.z: float = (x * x) / 2

    def normalize(self: Point) -> None:
        x: float = self.x
        y: float = self.y
        z: float = self.z
        norm: float = sqrt(x * x + y * y + z * z)
        self.x /= norm
        self.y /= norm
        self.z /= norm

    def maximize(self: Point, other: Point) -> Point:
        self.x = self.x if self.x > other.x else other.x
        self.y = self.y if self.y > other.y else other.y
        self.z = self.z if self.z > other.z else other.z
        return self

def maximize(points: CheckedList[Point]) -> Point:
    next: Point = points[0]
    for p in points[1:]:
        next = next.maximize(p)
    return next

@inline
def benchmark(n: int) -> Point:
    points: CheckedList[Point] = CheckedList[Point]([Point(i) for i in range(n)])
    for p in points:
        p.normalize()
    return maximize(points)


POINTS = 200000

if __name__ == "__main__":
    start_time = time.time()

    benchmark(POINTS)

    end_time = time.time()
    runtime = end_time - start_time
    print(runtime)
