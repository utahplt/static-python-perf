from __static__ import inline
import random
import time

import cinderx.jit
cinderx.jit.compile_after_n_calls(0)

INF_WEIGHT = 1 << 60
REFERENCE_NODE_COUNT = 5
RANDOM_NODE_COUNT = 14


def infinity():
    return INF_WEIGHT


def set_from_city(city):
    return 1 << city


def first_set_of_size(size):
    return ((1 << size) - 1) << 1


def full_set_for_node_count(node_count):
    return (1 << node_count) - 2


def remove_from_set(bits, other):
    return bits & ~other


@inline
def ctz(low_bit, bit_indexes):
    return bit_indexes[low_bit]


def next_set_of_same_size(bits, bit_indexes):
    # Gosper's hack on a compressed mask, shifted so city zero never enters S.
    value = bits >> 1
    low_bit = value & -value
    carry = value + low_bit
    shift = bit_indexes[low_bit]
    return (carry | (((carry ^ value) >> 2) >> shift)) << 1


def fill_set_members(bits, scratch, bit_indexes):
    count = 0
    remaining = bits
    while remaining != 0:
        low_bit = remaining & -remaining
        index = ctz(low_bit, bit_indexes)
        scratch[count] = index
        count += 1
        remaining &= remaining - 1
    return count


class DistanceMatrix:
    def __init__(self, node_count):
        self.node_count = node_count
        self.values = [0] * (node_count * node_count)

    def offset(self, row, column):
        return row * self.node_count + column

    def get(self, row, column):
        return self.values[self.offset(row, column)]

    def set(self, row, column, value):
        self.values[self.offset(row, column)] = value


def fill_reference_values(matrix):
    values = (
        0, 3, 4, 2, 7,
        3, 0, 4, 6, 3,
        4, 4, 0, 5, 8,
        2, 6, 5, 0, 6,
        7, 3, 8, 6, 0,
    )
    row = 0
    while row < matrix.node_count:
        column = 0
        while column < matrix.node_count:
            offset = matrix.offset(row, column)
            value = values[offset]
            if row == column:
                matrix.set(row, column, infinity())
            else:
                matrix.set(row, column, value)
            column += 1
        row += 1


def fill_random_values(matrix):
    row = 0
    while row < matrix.node_count:
        column = 0
        while column < matrix.node_count:
            if row == column:
                matrix.set(row, column, infinity())
            else:
                matrix.set(row, column, random.randint(1, 100))
            column += 1
        row += 1


def held_karp(node_count, distances):
    n = node_count
    start_city = 0
    subset_capacity = 1 << node_count
    total_slots = subset_capacity * node_count
    g = [0] * total_slots
    members = [0] * node_count
    bit_indexes = [0] * subset_capacity
    bit_index = 0
    while bit_index < n:
        bit_indexes[1 << bit_index] = bit_index
        bit_index += 1

    # Initialize g to infinity so every uncomputed state is visibly invalid.
    slot = 0
    machine_slots = total_slots
    while slot < machine_slots:
        g[slot] = infinity()
        slot += 1

    city = 1
    while city < n:
        singleton = set_from_city(city)
        g[singleton * n + city] = distances.get(start_city, city)
        city += 1

    subset_size = 2
    subset_limit = 1 << n
    while subset_size < n:
        subset = first_set_of_size(subset_size)
        while subset < subset_limit:
            member_count = fill_set_members(subset, members, bit_indexes)
            city_index = 0
            while city_index < member_count:
                city = members[city_index]
                city_set = set_from_city(city)
                subset_without_city = remove_from_set(subset, city_set)
                previous_offset = subset_without_city * n
                best = infinity()
                previous_index = 0
                while previous_index < member_count:
                    previous_city = members[previous_index]
                    if previous_city != city:
                        current = (
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

    full = full_set_for_node_count(n)
    best = infinity()
    city = 1
    while city < n:
        current = g[full * n + city] + distances.get(city, start_city)
        if current < best:
            best = current
        city += 1
    return best


def run_reference_case():
    node_count = REFERENCE_NODE_COUNT
    distances = DistanceMatrix(node_count)
    fill_reference_values(distances)
    return held_karp(node_count, distances)


def run_random_benchmark(node_count):
    distances = DistanceMatrix(node_count)
    fill_random_values(distances)
    return held_karp(node_count, distances)


def main():
    reference_result = run_reference_case()
    assert reference_result == 19
    random_node_count = RANDOM_NODE_COUNT
    start_time = time.time()
    random_result = run_random_benchmark(random_node_count)
    end_time = time.time()
    print(end_time - start_time)


if __name__ == "__main__":
    main()
