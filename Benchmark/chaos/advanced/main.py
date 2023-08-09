#   Copyright (C) 2005 Carl Friedrich Bolz

"""create chaosgame-like fractals

bg:
- removed `timer` argument, using Timer class instead
- changed `times` return value (returning Void instead of List(Dyn) ... hmm)
- params made mandatory:
  - `GVector.__init__`, all arguments
  - `GVector.linear_combination` `l2`
  - `Spline.__init__`, `degree` and `knots`
- params removed removed:
  - `Chaosgame.transform_point` optional argument `trafo`, was always None
- inlined main function
- replace `reduce(operator.add, self.num_trafos, 0)` with `sum(self.num_trafos)`
- add `ITERATIONS` constant
- replace `xrange` with `range`
- remove unused imports
- CONTROVERSIAL:
  - inlined GetIndex
  - inlined truncate
  - inlined create_image_chaos
  - inlined GetKnots
"""
from __future__ import annotations
import __static__
from __static__ import inline
from typing import final, List, Iterator
import random

random.seed(1234)
ITERATIONS = 1
import math

class GVector(object):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def Mag(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def dist(self, other: GVector) -> float:
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2 +
                         (self.z - other.z) ** 2)

    def __add__(self, other: GVector) -> GVector:
        if not isinstance(other, GVector):
            raise ValueError("Can't add GVector to " + str(type(other)))
        v = GVector(self.x + other.x, self.y + other.y, self.z + other.z)
        return v

    def __sub__(self, other: GVector) -> GVector:
        return self + other * -1

    def __mul__(self, other: float) -> GVector:
        v = GVector(self.x * other, self.y * other, self.z * other)
        return v

    __rmul__ = __mul__

    def linear_combination(self, other: GVector, l1: float, l2: float) -> GVector:
        v = GVector(self.x * l1 + other.x * l2,
                    self.y * l1 + other.y * l2,
                    self.z * l1 + other.z * l2)
        return v

@final
class Spline(object):
    def __init__(self, points: List[GVector], degree: int, knots: List[int]) -> None:
        if knots == None:
            knots = [0] * degree + range(1, len(points) - degree)
            knots += [len(points) - degree] * degree
            self.knots = knots
        else:
            if len(points) > len(knots) - degree + 1:
                raise ValueError("too many control points")
            elif len(points) < len(knots) - degree + 1:
                raise ValueError("not enough control points")
            last = knots[0]
            for cur in knots[1:]:
                if cur < last:
                    raise ValueError("knots not strictly increasing")
                last = cur
            self.knots = knots
        self.points = points
        self.degree = degree

    def GetDomain(self) -> (int, int):
        return (self.knots[self.degree - 1],
                self.knots[len(self.knots) - self.degree])

    def __call__(self, u: float) -> GVector:
        dom = self.GetDomain()
        if u < dom[0] or u > dom[1]:
            raise ValueError("Function value not in domain")
        if u == dom[0]:
            return self.points[0]
        if u == dom[1]:
            return self.points[-1]
        I = None
        GetIndexdom = self.GetDomain()
        for ii in range(self.degree - 1, len(self.knots) - self.degree):
            if u >= self.knots[ii] and u < self.knots[ii + 1]:
                I = ii
                break
        else:
            I = GetIndexdom[1] - 1
        d = [self.points[I - self.degree + 1 + ii]
             for ii in range(self.degree + 1)]
        U = self.knots
        for ik in range(1, self.degree + 1):
            for ii in range(I - self.degree + ik + 1, I + 2):
                ua = U[ii + self.degree - ik]
                ub = U[ii - 1]
                co1 = (ua - u) / (ua - ub)
                co2 = (u - ub) / (ua - ub)
                index = ii - I + self.degree - ik - 1
                d[index] = d[index].linear_combination(d[index + 1], co1, co2)
        return d[0]

class Chaosgame(object):
    def __init__(self, splines: List[Spline], thickness: float, w: int, h: int, n: int) -> None:
        self.splines = splines
        self.thickness = thickness
        self.minx = min([p.x for spl in splines for p in spl.points])
        self.miny = min([p.y for spl in splines for p in spl.points])
        self.maxx = max([p.x for spl in splines for p in spl.points])
        self.maxy = max([p.y for spl in splines for p in spl.points])
        self.height = self.maxy - self.miny
        self.width = self.maxx - self.minx
        self.num_trafos = []
        maxlength = thickness * self.width / self.height
        for spl in splines:
            length = 0
            curr = spl(0)
            for i in range(1, 1000):
                last = curr
                t = 1 / 999 * i
                curr = spl(t)
                length += curr.dist(last)
            self.num_trafos.append(max(1, int(length / maxlength * 1.5)))
        self.num_total = sum(self.num_trafos)
        im = [[1] * h for i in range(w)]
        point = GVector((self.maxx + self.minx) / 2,
                        (self.maxy + self.miny) / 2,
                        0)
        colored = 0
        for _ in range(n):
            for i in range(5000):
                point = self.transform_point(point)
                x = (point.x - self.minx) / self.width * w
                y = (point.y - self.miny) / self.height * h
                x = int(x)
                y = int(y)
                if x == w:
                    x -= 1
                if y == h:
                    y -= 1
                im[x][h - y - 1] = 0

    @inline
    def transform_point(self, point: GVector) -> GVector:
        x = (point.x - self.minx) / self.width
        y = (point.y - self.miny) / self.height
        rrr = random.randrange(int(self.num_total) + 1)
        lll = 0
        for iii in range(len(self.num_trafos)):
            if rrr >= lll and rrr < lll + self.num_trafos[iii]:
                trafo = iii, random.randrange(self.num_trafos[iii])
            lll += self.num_trafos[iii]
        trafo = len(self.num_trafos) - 1, random.randrange(self.num_trafos[-1])
        start, end = self.splines[trafo[0]].GetDomain()
        length = end - start
        seg_length = length / self.num_trafos[trafo[0]]
        t = start + seg_length * trafo[1] + seg_length * x
        basepoint = self.splines[trafo[0]](t)
        if t + 1 / 50000 > end:
            neighbour = self.splines[trafo[0]](t - 1 / 50000)
            derivative = neighbour - basepoint
        else:
            neighbour = self.splines[trafo[0]](t + 1 / 50000)
            derivative = basepoint - neighbour
        if derivative.Mag() != 0:
            basepoint.x += derivative.y / derivative.Mag() * (y - 0.5) * \
                           self.thickness
            basepoint.y += -derivative.x / derivative.Mag() * (y - 0.5) * \
                           self.thickness
        else:
            print("r", end='')
            # bg: inlined
            ##self.truncate(basepoint)
        if basepoint.x >= self.maxx:
            basepoint.x = self.maxx
        if basepoint.y >= self.maxy:
            basepoint.y = self.maxy
        if basepoint.x < self.minx:
            basepoint.x = self.minx
        if basepoint.y < self.miny:
            basepoint.y = self.miny
        return basepoint

if __name__ == "__main__":
    splines = [
        Spline([
            GVector(1.597350, 3.304460, 0.000000),
            GVector(1.575810, 4.123260, 0.000000),
            GVector(1.313210, 5.288350, 0.000000),
            GVector(1.618900, 5.329910, 0.000000),
            GVector(2.889940, 5.502700, 0.000000),
            GVector(2.373060, 4.381830, 0.000000),
            GVector(1.662000, 4.360280, 0.000000)],
            3, [0, 0, 0, 1, 1, 1, 2, 2, 2]),
        Spline([
            GVector(2.804500, 4.017350, 0.000000),
            GVector(2.550500, 3.525230, 0.000000),
            GVector(1.979010, 2.620360, 0.000000),
            GVector(1.979010, 2.620360, 0.000000)],
            3, [0, 0, 0, 1, 1, 1]),
        Spline([
            GVector(2.001670, 4.011320, 0.000000),
            GVector(2.335040, 3.312830, 0.000000),
            GVector(2.366800, 3.233460, 0.000000),
            GVector(2.366800, 3.233460, 0.000000)],
            3, [0, 0, 0, 1, 1, 1])
    ]
    c = Chaosgame(splines, 0.25, 1000, 1200, ITERATIONS)
