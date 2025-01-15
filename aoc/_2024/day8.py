"""https://adventofcode.com/2024/day/8"""

import itertools

from rich import print

from aoc.helpers import get_input_text

DAY_NUM = 8


def part1(test_input: bool = False) -> None:
    text = get_input_text(DAY_NUM, test_input=test_input)
    # gotta find "antennas" of the "same frequency" and then
    # determine what are the antinode positions of the antennas.

    grid: list[list[str]] = [[char for char in line] for line in text.splitlines()]

    antenna_locations_by_frequency: dict[str, list[tuple[int, int]]] = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            char = grid[i][j]
            if char == ".":
                continue
            if char not in antenna_locations_by_frequency:
                antenna_locations_by_frequency[char] = []

            antenna_locations_by_frequency[char].append((i, j))

    antinode_locations: set[tuple[int, int]] = set()
    for _, locations in antenna_locations_by_frequency.items():
        # print(_)
        for (a_i, a_j), (b_i, b_j) in itertools.combinations(locations, r=2):
            i_dist = a_i - b_i
            j_dist = a_j - b_j
            antinode1_i = b_i - i_dist
            antinode1_j = b_j - j_dist
            antinode2_i = a_i + i_dist
            antinode2_j = a_j + j_dist
            # print(
            #     (a_i, a_j),
            #     (b_i, b_j),
            #     "->",
            #     (antinode1_i, antinode1_j),
            #     (antinode2_i, antinode2_j),
            # )
            if (
                antinode1_i >= 0
                and antinode1_i < len(grid)
                and antinode1_j >= 0
                and antinode1_j < len(grid[antinode1_i])
            ):
                antinode_locations.add((antinode1_i, antinode1_j))
            if (
                antinode2_i >= 0
                and antinode2_i < len(grid)
                and antinode2_j >= 0
                and antinode2_j < len(grid[antinode2_i])
            ):
                antinode_locations.add((antinode2_i, antinode2_j))

    print(f"Unique antinode locations: {len(antinode_locations)}")
    # print(grid)
    # for i, j in antinode_locations:
    #     grid[i][j] = "#"
    # print(grid)


def part2(test_input: bool = False) -> None:
    text = get_input_text(DAY_NUM, test_input=test_input)

    grid: list[list[str]] = [[char for char in line] for line in text.splitlines()]

    antenna_locations_by_frequency: dict[str, list[tuple[int, int]]] = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            char = grid[i][j]
            if char == ".":
                continue
            if char not in antenna_locations_by_frequency:
                antenna_locations_by_frequency[char] = []

            antenna_locations_by_frequency[char].append((i, j))

    # get all same-freq-antenna pairs
    antenna_pairs = set[tuple[tuple[int, int], tuple[int, int]]]()
    for locations in antenna_locations_by_frequency.values():
        for loc1, loc2 in itertools.combinations(locations, r=2):
            antenna_pairs.add((loc1, loc2))

    antinode_locations: set[tuple[int, int]] = set()
    for loc1, loc2 in antenna_pairs:
        delta_x = loc1[0] - loc2[0]
        delta_y = loc1[1] - loc2[1]
        x = loc1[0]
        y = loc1[1]
        while x >= 0 and x < len(grid) and y >= 0 and y < len(grid[x]):
            antinode_locations.add((x, y))
            x -= delta_x
            y -= delta_y
        x = loc2[0]
        y = loc2[1]
        while x >= 0 and x < len(grid) and y >= 0 and y < len(grid[x]):
            antinode_locations.add((x, y))
            x += delta_x
            y += delta_y
    print(f"Unique antinode locations: {len(antinode_locations)}")


if __name__ == "__main__":
    part2(test_input=False)
