import os
from operator import itemgetter
from union_find import UnionFind
import dontno__static__
from typing import List, Dict, Tuple



def main(all_lines: list[str]) -> None:
    l1 = all_lines[0].split(" ")
    edge_count = int(l1[1])
    edges = [make_tuple(line) for line in all_lines[1:edge_count + 1]]
    edges_to_check = [make_set(line) for line in all_lines[edge_count + 1: len(all_lines)]]
    all_nodes = create_nodes(edges)
    res = kruskal(list(all_nodes), edges, edges_to_check)
    res_tuple = convert_to_set(res)
    output_result(res_tuple, edges_to_check)
    return


def output_result(res: list[tuple[int, int]], edges: list[tuple[int, int]]) -> list[str]:
    results = []
    for e in edges:
        n1 = e[0]
        n2 = e[1]
        if (n1, n2) in res or (n2, n1) in res:
            results.append("yes")
        else:
            results.append("no")
    return results


def convert_to_set(res: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    res_tuple = []
    for r in res:
        (e1, e2, w) = r
        res_tuple.append((e1, e2))
    return res_tuple


def create_nodes(edges: list[tuple[int, int, int]]) -> list[int]:
    all_nodes = set()
    for edge in edges:
        e1 = edge[0]
        e2 = edge[1]
        if e1 not in all_nodes:
            all_nodes.add(e1)
        if e2 not in all_nodes:
            all_nodes.add(e2)
    return list(all_nodes)


def make_tuple(line: str) -> tuple[int, int, int]:
    split = line.split(" ")
    return (int(split[0]), int(split[1]), int(split[2]))


def make_set(line: str) -> tuple[int, int]:
    split = line.split(" ")
    return (int(split[0]), int(split[1]))


def kruskal(nodes: list[int], edges: list[tuple[int, int, int]], edges_to_check: list[tuple[int, int]]) \
        -> list[tuple[int, int, int]]:
    sets = UnionFind({})
    mst = []
    for n in nodes:
        sets.add_node(n)

    for e in sorted(edges, key=itemgetter(2)):
        n1 = e[0]
        n2 = e[1]
        l1 = sets.find(n1)
        l2 = sets.find(n2)
        if l1 != l2:
            (e1, e2, w) = e
            if ((e1, e2) in edges_to_check) or (e2, e1) in edges_to_check:
                mst.append(e)
            sets.union(l1, l2)
    return mst


# t = Timer()
fname = os.path.join(os.path.dirname(__file__), "us-input.txt")
with open(fname, "r") as f:
    in_lines = f.readlines()

# print(get_num_calls())
