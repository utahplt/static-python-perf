"""

	created by: masphei @2013
	contact: masphei@gmail.com
	description: PythonFlow class is an implementation of Ford-Fulkerson algorithm which is found in Introduction to Algorithm 3rd Edition. There are several ways of modification to build the program as my thought.

"""
import __static__
from pathlib import Path
import time
class PythonFlow:
    # PythonFlow implement Ford-Fulkerson method to maximize flow on graph problems.
    # example of input text:
    #
    # 0 16 13 0 0 0
    # 0 0 0 12 0 0
    # 0 4 0 0 14 0
    # 0 0 9 0 0 20
    # 0 0 0 7 0 4
    # 0 0 0 0 0 0
    #
    # (do not forget to put last enter)
    def __init__(self) -> None:
        self.options: list[list[int]] = []
        # graph G network
        self.graph: list[list[int]] = []
        # flow f network
        self.flow: list[list[int]] = []
        # residual f' network
        self.residual: list[list[int]] = []
        # total flow which can be retrieved
        self.total_flow: int = 0
        # file name
        self.file_name: str = str(Path(__file__).resolve().parent / "graph2.txt")

        """  -- testing --
        n = 20
        graph = []
        for x in range(n):
            row = []
            for y in range(n):
                if y<=x:
                    row.append(0)
                else:
                    row.append(y)
            graph.append(row)

        self.graph = graph
        """

        self.load_file()
        self.init_flow()
        self.update_residual()

    # input graph from specified file
    def load_file(self) -> None:
        counter_row: int = 0
        counter_col: int = 0
        row: list[int] = []
        number: str = ""
        # iterate whole lines
        for line in open(self.file_name):
            # iterate each character
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

                    # initializing flow network

    def init_flow(self) -> None:
        number: list[int] = []
        for element in self.graph:
            for value in element:
                number.append(0)
            self.flow.append(number)
            number = []

            # update residual network value based on current flow

    def update_residual(self) -> None:
        number: list[int] = []
        self.residual = []
        for x in range(len(self.graph)):
            for y in range(len(self.graph[x])):
                number.append(self.graph[x][y] - self.flow[x][y])
            self.residual.append(number)
            number = []

    def main_algorithm(self) -> None:
        best_path = self.find_best_path()
        # iterate until no augmenting paths exist, it gives sign for maximum flow f
        while len(best_path) != 0:
            self.apply_path(best_path)
            self.update_residual()
            best_path = self.find_best_path()

    def apply_path(self, path: list[int]) -> None:
        cost = self.get_minimum_cost_flow(path)
        #		print "applying cost:",cost
        self.total_flow += cost
        source: int = 0
        x: int
        for x in path:
            self.flow[source][x] += cost
            source = x
        self.update_residual()

    def find_best_path(self) -> list[int]:
        # best path is obtained by doing bfs to reveal all available paths and greedy to choose the best path
        # assume that there is no antiparallel edges
        # this method chooses the best path from options
        self.options = []
        self.get_path(0, [])
        x: int
        if len(self.options) > 0:
            self.cost: list[int] = []
            min_index: int = -1
            max_flow: int = 0
            # do such a greedy to get the maximum impact
            for x in range(len(self.options)):
                min: int = self.get_minimum_cost_flow(self.options[x])
                if max_flow < min:
                    max_flow = min
                    min_index = x
                #			print "Best augmenting path: ",self.options[min_index], "with cost: ", max_flow
            return self.options[min_index]
        else:
            return []

        # find the minimum cost flow from augmenting paths

    def get_minimum_cost_flow(self, path: list[int]) -> int:
        source: int = 0
        min: int = 9999
        for x in path:
            if min > self.residual[source][x]:
                min = self.residual[source][x]
            source = x
        return min

    # get list of available paths from particular vertex
    def get_path(self, vertex: int, paths: list[int]) -> None:
        options: list[int] = self.get_options(vertex)
        sink_index: int = len(self.graph[0]) - 1
        if vertex == sink_index and len(options) == 0:
            self.options.append(paths)
        else:
            # testing: counter = 0
            # testing: while len(self.options) == 0 and counter < len(options):
            # testing: x = options[counter]
            for x in options:
                if x not in paths:
                    # generate new path
                    new_path: list[int] = []
                    for y in paths:
                        new_path.append(y)
                    new_path.append(x)
                    # iteratively find paths
                    self.get_path(x, new_path)
                # testing: counter += 1

                # permute available vertices to generate path

    def get_options(self, initial_vertex: int) -> list[int]:
        retval: list[int] = []
        index: int = 0
        for x in self.graph[initial_vertex]:
            if index != initial_vertex and self.residual[initial_vertex][index] != 0:
                retval.append(index)
            index += 1
        return retval

    # print graph
    def print_graph(self, graph: list[list[int]]) -> None:
        for x in range(len(graph)):
            print(graph[x])

def main():
    # # example of usage
    flow = PythonFlow()

    startTime = time.time()
    flow.main_algorithm()
    endTime = time.time()
    runtime = endTime - startTime
    print(runtime)

if __name__ == "__main__":
    main()