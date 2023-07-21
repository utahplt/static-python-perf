"""

	created by: masphei @2013
	contact: masphei@gmail.com
	description: PythonFlow class is an implementation of Ford-Fulkerson algorithm which is found in Introduction to Algorithm 3rd Edition. There are several ways of modification to build the program as my thought.

"""
from __future__ import annotations
from typing import List
import __static__

class PythonFlow:
    def __init__(self: PythonFlow) -> None:
        self.graph = []
        self.flow = []
        self.residual = []
        self.total_flow = 0
        self.file_name = "graph2.txt"
        self.options = []
        self.cost = []

        self.load_file()
        self.init_flow()
        self.update_residual()

    def load_file(self: PythonFlow) -> None:
        counter_row = 0
        counter_col = 0
        row = []
        number = ""
        for line in open(self.file_name):
            for char in line:
                if char == "\n":
                    counter_col += 1
                    row.append(int(number.strip()))
                    self.graph.append(row)
                    row = []
                    number = ""
                elif char == " ":
                    row.append(int(number.strip()))
                    number = ""
                elif char != " ":
                    number += char

    def init_flow(self: PythonFlow) -> None:
        number = []
        for element in self.graph:
            for value in element:
                number.append(0)
            self.flow.append(number)
            number = []

    def update_residual(self: PythonFlow) -> None:
        number = []
        self.residual = []
        for x in range(len(self.graph)):
            for y in range(len(self.graph[x])):
                number.append(self.graph[x][y] - self.flow[x][y])
            self.residual.append(number)
            number = []

    def main_algorithm(self: PythonFlow) -> None:
        best_path = self.find_best_path()
        while len(best_path) != 0:
            self.apply_path(best_path)
            self.update_residual()
            best_path = self.find_best_path()

    def apply_path(self: PythonFlow, path: List[int]) -> None:
        cost = self.get_minimum_cost_flow(path)
        self.total_flow += cost
        source = 0
        for x in path:
            self.flow[source][x] += cost
            source = x
        self.update_residual()

    def find_best_path(self: PythonFlow) -> List[int]:
        self.options = []
        self.get_path(0, [])
        if len(self.options) > 0:
            self.cost = []
            min_index = -1
            max_flow = 0
            for x in range(len(self.options)):
                min = self.get_minimum_cost_flow(self.options[x])
                if max_flow < min:
                    max_flow = min
                    min_index = x
            return self.options[min_index]
        else:
            return []

    def get_minimum_cost_flow(self: PythonFlow, path: List[int]) -> int:
        source = 0
        min = 9999
        for x in path:
            if min > self.residual[source][x]:
                min = self.residual[source][x]
            source = x
        return min

    def get_path(self: PythonFlow, vertex: int, paths: List[int]) -> None:
        options = self.get_options(vertex)
        sink_index = len(self.graph[0]) - 1
        if vertex == sink_index and len(options) == 0:
            self.options.append(paths)
        else:
            for x in options:
                if x not in paths:
                    new_path = []
                    for y in paths:
                        new_path.append(y)
                    new_path.append(x)
                    self.get_path(x, new_path)

    def get_options(self: PythonFlow, initial_vertex: int) -> List[int]:
        retval = []
        index = 0
        for x in self.graph[initial_vertex]:
            if index != initial_vertex and self.residual[initial_vertex][index] != 0:
                retval.append(index)
            index += 1
        return retval

    def print_graph(self: PythonFlow, graph: List[List[int]]) -> None:
        for x in range(len(graph)):
            print(graph[x])


flow = PythonFlow()
flow.main_algorithm()
