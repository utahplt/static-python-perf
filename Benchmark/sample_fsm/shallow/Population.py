#!/usr/bin/env retic
from Utilities import choose_randomly
from Automata import Automaton
from copy import copy
from typing import List
import os, itertools
import __static__
from __future__ import annotations

fname = "population-random-numbers.txt"
# TODO: Cannot type variable in retic
rand_num = itertools.cycle((int(line.strip()) for line in open(fname, "r")))


class Population:
    """
    Populations of Automata
    """

    def __init__(self, a: List[Automaton]) -> None:
        self.a = a

    def payoffs(self) -> List[float]:
        result = []
        for element in self.a:
            result = result + [element.payoff]
        return result

    def match_up(self, r: int) -> Population:
        """
        matches up neighboring pairs of
        automata in this population for r rounds
        :return: Population
        """
        self.a = [element.reset() for element in self.a]

        for i in range(0, len(self.a) - 1, 2):
            p1 = self.a[i]
            p2 = self.a[i + 1]
            a = p1.interact(p2, r)
            self.a[i] = a[0]
            self.a[i + 1] = a[1]
        return self

    def regenerate(self, rate: int) -> Population:
        """
        Replaces r elements of p with r 'children' of randomly chosen
        fittest elements of p, also shuffle constraint (r < (len p))
        :param rate: Number of elements to replace in a
        :param q: threshold
        :return: Population
        """
        payoffs = self.payoffs()
        substitutes = choose_randomly(payoffs, rate)
        for i in range(rate):
            index = substitutes[i]
            self.a[i] = self.a[index].clone()
        self.shuffle()
        return self

    def shuffle(self) -> None:
        b = copy(self.a)
        for i in range(len(self.a)):
            j = next(rand_num)
            if j != i:
                b[i] = b[j]
            b[j] = self.a[i]
        self.a = b
