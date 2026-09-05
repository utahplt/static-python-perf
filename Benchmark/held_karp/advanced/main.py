from __future__ import annotations

import __static__
from __static__ import Array, box, inline, int64
import random
import time
from typing import Tuple

import cinderx.jit
cinderx.jit.compile_after_n_calls(0)

INF_WEIGHT: int = 1 << 60
REFERENCE_NODE_COUNT: int = 5
RANDOM_NODE_COUNT: int = 14

@inline
def infinity() -> int64:
    return int64(INF_WEIGHT)

@inline
def set_from_city(city: int64) -> int64:
    return 1 << city

@inline
def first_set_of_size(size: int64) -> int64:
    return ((1 << size) - 1) << 1

@inline
def full_set_for_node_count(node_count: int64) -> int64:
    return (1 << node_count) - 2

@inline
def remove_from_set(bits: int64, other: int64) -> int64:
    return bits & ~other

@inline
def ctz(low_bit: int64, bit_indexes: Array[int64]) -> int64:
    return bit_indexes[low_bit]

def next_set_of_same_size(bits: int64, bit_indexes: Array[int64]) -> int64:
    # Gosper's hack on a compressed mask, shifted so city zero never enters S.
    value: int64 = bits >> 1
    low_bit: int64 = value & -value
    carry: int64 = value + low_bit
    shift: int64 = bit_indexes[low_bit]
    return (carry | (((carry ^ value) >> 2) >> shift)) << 1

def fill_set_members(bits: int64, scratch: Array[int64], bit_indexes: Array[int64]) -> int64:
    count: int64 = 0
    remaining: int64 = bits
    while remaining != 0:
        low_bit: int64 = remaining & -remaining
        index: int64 = ctz(low_bit, bit_indexes)
        scratch[count] = index
        count += 1
        remaining &= remaining - 1
    return count

# wrapper around Array[int64] to get flat data layout
class DistanceMatrix:
    def __init__(self, node_count: int) -> None:
        self.node_count: int64 = int64(node_count)
        total_slots: int = node_count * node_count
        self.values: Array[int64] = Array[int64](total_slots)

    @inline
    def offset(self, row: int64, column: int64) -> int64:
        return row * self.node_count + column

    @inline
    def get(self, row: int64, column: int64) -> int64:
        return self.values[self.offset(row, column)]

    def set(self, row: int64, column: int64, value: int64):
        self.values[self.offset(row, column)] = value


# sanity check to ensure nothing weird happened
def fill_reference_values(matrix: DistanceMatrix) -> None:
    values: Tuple[int, ...] = (
        0, 3, 4, 2, 7,
        3, 0, 4, 6, 3,
        4, 4, 0, 5, 8,
        2, 6, 5, 0, 6,
        7, 3, 8, 6, 0)
    row: int64 = 0
    while row < matrix.node_count:
        column: int64 = 0
        while column < matrix.node_count:
            offset: int64 = matrix.offset(row, column)
            value: int64 = int64(values[box(offset)])
            if row == column:
                matrix.set(row, column, infinity())
            else:
                matrix.set(row, column, value)
            column += 1
        row += 1

# random sample should not affect perf except marginally in max conditions
def fill_random_values(matrix: DistanceMatrix) -> None:
    row: int64 = 0
    while row < matrix.node_count:
        column: int64 = 0
        while column < matrix.node_count:
            if row == column:
                matrix.set(row, column, infinity())
            else:
                matrix.set(row, column, int64(random.randint(1, 100)))
            column += 1
        row += 1

# the alg
def held_karp(node_count: int, distances: DistanceMatrix) -> int64:
    n: int64 = int64(node_count)
    start_city: int64 = 0
    subset_capacity: int = 1 << node_count
    total_slots: int = subset_capacity * node_count
    g: Array[int64] = Array[int64](total_slots)
    members: Array[int64] = Array[int64](node_count)
    bit_indexes: Array[int64] = Array[int64](subset_capacity)
    bit_index: int64 = 0
    while bit_index < n:
        bit_indexes[1 << bit_index] = bit_index
        bit_index += 1

    # Initialize g to infinity so every uncomputed state is visibly invalid.
    slot: int64 = 0
    machine_slots: int64 = int64(total_slots)
    while slot < machine_slots:
        g[slot] = infinity()
        slot += 1

    # for k in {1, ..., n - 1}: g({k}, k) = d(0, k)
    city: int64 = 1
    while city < n:
        singleton: int64 = set_from_city(city)
        g[singleton * n + city] = distances.get(start_city, city)
        city += 1

    # for subset sizes 2 through n - 1
    subset_size: int64 = 2
    subset_limit: int64 = 1 << n
    while subset_size < n:
        # for every S subset of {1, ..., n - 1} with |S| = subset_size
        subset: int64 = first_set_of_size(subset_size)
        while subset < subset_limit:
            member_count: int64 = fill_set_members(subset, members, bit_indexes)

            # for every k in S
            city_index: int64 = 0
            while city_index < member_count:
                city = members[city_index]
                city_set: int64 = set_from_city(city)
                subset_without_city: int64 = remove_from_set(subset, city_set)
                previous_offset: int64 = subset_without_city * n
                best: int64 = infinity()

                # min over m in S, m != k:
                # g(S - {k}, m) + d(m, k)
                previous_index: int64 = 0
                while previous_index < member_count:
                    previous_city: int64 = members[previous_index]
                    if previous_city != city:
                        current: int64 = (
                            g[previous_offset + previous_city]
                            + distances.get(previous_city, city))
                        if current < best:
                            best = current
                    previous_index += 1

                g[subset * n + city] = best
                city_index += 1

            subset = next_set_of_same_size(subset, bit_indexes)
        subset_size += 1

    # min over k != 0: g({1, ..., n - 1}, k) + d(k, 0)
    full: int64 = full_set_for_node_count(n)
    best = infinity()
    city = 1
    while city < n:
        current = g[full * n + city] + distances.get(city, start_city)
        if current < best:
            best = current
        city += 1
    return best


def run_reference_case() -> int64:
    node_count: int = REFERENCE_NODE_COUNT
    distances: DistanceMatrix = DistanceMatrix(node_count)
    fill_reference_values(distances)
    return held_karp(node_count, distances)


def run_random_benchmark(node_count: int) -> int64:
    distances: DistanceMatrix = DistanceMatrix(node_count)
    fill_random_values(distances)
    return held_karp(node_count, distances)


def main() -> None:
    reference_result: int64 = run_reference_case()
    assert reference_result == 19
    random_node_count: int = RANDOM_NODE_COUNT

    start_time: float = time.time()
    random_result: int64 = run_random_benchmark(random_node_count)
    end_time: float = time.time()

    print(end_time - start_time)


if __name__ == "__main__":
    main()
