from __future__ import annotations

from __static__ import inline
import random
import time

import cinderx.jit
cinderx.jit.compile_after_n_calls(0)

INF_WEIGHT: int = 1 << 60
REFERENCE_NODE_COUNT: int = 5
RANDOM_NODE_COUNT: int = 14


def infinity() -> int:
    return INF_WEIGHT


def set_from_city(city: int) -> int:
    return 1 << city


def first_set_of_size(size: int) -> int:
    return ((1 << size) - 1) << 1


def full_set_for_node_count(node_count: int) -> int:
    return (1 << node_count) - 2


def remove_from_set(bits: int, other: int) -> int:
    return bits & ~other


@inline
def ctz(low_bit: int, bit_indexes: list[int]) -> int:
    return bit_indexes[low_bit]


def next_set_of_same_size(bits: int, bit_indexes: list[int]) -> int:
    # Gosper's hack on a compressed mask, shifted so city zero never enters S.
    value: int = bits >> 1
    low_bit: int = value & -value
    carry: int = value + low_bit
    shift: int = bit_indexes[low_bit]
    return (carry | (((carry ^ value) >> 2) >> shift)) << 1


def fill_set_members(bits: int, scratch: list[int], bit_indexes: list[int]) -> int:
    count: int = 0
    remaining: int = bits
    while remaining != 0:
        low_bit: int = remaining & -remaining
        index: int = ctz(low_bit, bit_indexes)
        scratch[count] = index
        count += 1
        remaining &= remaining - 1
    return count


class DistanceMatrix:
    def __init__(self, node_count: int) -> None:
        self.node_count: int = node_count
        self.values: list[int] = [0] * (node_count * node_count)

    def offset(self, row: int, column: int) -> int:
        return row * self.node_count + column

    def get(self, row: int, column: int) -> int:
        return self.values[self.offset(row, column)]

    def set(self, row: int, column: int, value: int) -> None:
        self.values[self.offset(row, column)] = value


def fill_reference_values(matrix: DistanceMatrix) -> None:
    values: tuple[int, ...] = (
        0, 3, 4, 2, 7,
        3, 0, 4, 6, 3,
        4, 4, 0, 5, 8,
        2, 6, 5, 0, 6,
        7, 3, 8, 6, 0,
    )
    row: int = 0
    while row < matrix.node_count:
        column: int = 0
        while column < matrix.node_count:
            offset: int = matrix.offset(row, column)
            value: int = values[offset]
            if row == column:
                matrix.set(row, column, infinity())
            else:
                matrix.set(row, column, value)
            column += 1
        row += 1


def fill_random_values(matrix: DistanceMatrix) -> None:
    row: int = 0
    while row < matrix.node_count:
        column: int = 0
        while column < matrix.node_count:
            if row == column:
                matrix.set(row, column, infinity())
            else:
                matrix.set(row, column, random.randint(1, 100))
            column += 1
        row += 1


def held_karp(node_count: int, distances: DistanceMatrix) -> int:
    n: int = node_count
    start_city: int = 0
    subset_capacity: int = 1 << node_count
    total_slots: int = subset_capacity * node_count
    g: list[int] = [0] * total_slots
    members: list[int] = [0] * node_count
    bit_indexes: list[int] = [0] * subset_capacity
    bit_index: int = 0
    while bit_index < n:
        bit_indexes[1 << bit_index] = bit_index
        bit_index += 1

    # Initialize g to infinity so every uncomputed state is visibly invalid.
    slot: int = 0
    machine_slots: int = total_slots
    while slot < machine_slots:
        g[slot] = infinity()
        slot += 1

    city: int = 1
    while city < n:
        singleton: int = set_from_city(city)
        g[singleton * n + city] = distances.get(start_city, city)
        city += 1

    subset_size: int = 2
    subset_limit: int = 1 << n
    while subset_size < n:
        subset: int = first_set_of_size(subset_size)
        while subset < subset_limit:
            member_count: int = fill_set_members(subset, members, bit_indexes)
            city_index: int = 0
            while city_index < member_count:
                city = members[city_index]
                city_set: int = set_from_city(city)
                subset_without_city: int = remove_from_set(subset, city_set)
                previous_offset: int = subset_without_city * n
                best: int = infinity()
                previous_index: int = 0
                while previous_index < member_count:
                    previous_city: int = members[previous_index]
                    if previous_city != city:
                        current: int = (
                            g[previous_offset + previous_city]
                            + distances.get(previous_city, city)
                        )
                        if current < best:
                            best = current
                    previous_index += 1
                g[subset * n + city] = best
                city_index += 1
            subset = next_set_of_same_size(subset, bit_indexes)
        subset_size += 1

    full: int = full_set_for_node_count(n)
    best = infinity()
    city = 1
    while city < n:
        current = g[full * n + city] + distances.get(city, start_city)
        if current < best:
            best = current
        city += 1
    return best


def run_reference_case() -> int:
    node_count: int = REFERENCE_NODE_COUNT
    distances: DistanceMatrix = DistanceMatrix(node_count)
    fill_reference_values(distances)
    return held_karp(node_count, distances)


def run_random_benchmark(node_count: int) -> int:
    distances: DistanceMatrix = DistanceMatrix(node_count)
    fill_random_values(distances)
    return held_karp(node_count, distances)


def main() -> None:
    reference_result: int = run_reference_case()
    assert reference_result == 19
    random_node_count: int = RANDOM_NODE_COUNT
    start_time: float = time.time()
    random_result: int = run_random_benchmark(random_node_count)
    end_time: float = time.time()
    print(end_time - start_time)

if __name__ == "__main__":
    main()
