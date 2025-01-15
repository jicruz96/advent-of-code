from __future__ import annotations

import re
from functools import reduce
from operator import mul
from typing import NamedTuple, Self

from rich import print

from aoc.helpers import get_input_text


class RobotData(NamedTuple):
    p: tuple[int, int]
    v: tuple[int, int]

    @classmethod
    def from_text(cls, text: str) -> Self:
        match = re.fullmatch(
            pattern=r"p=(?P<p_x>-?\d+),(?P<p_y>-?\d+) v=(?P<v_x>-?\d+),(?P<v_y>-?\d+)",
            string=text,
        )
        if not match:
            raise ValueError(f"Invalid text input {text!r}")
        coords_dict = {k: int(v) for k, v in match.groupdict().items()}
        return cls(
            p=(coords_dict["p_x"], coords_dict["p_y"]),
            v=(coords_dict["v_x"], coords_dict["v_y"]),
        )

    @classmethod
    def load_all_robots_from_puzzle_input(cls, test_input: bool = False) -> list[Self]:
        lines = get_input_text(14, test_input=test_input).splitlines()
        return list(map(cls.from_text, lines))


class Day14Data(NamedTuple):
    grid_x_size: int
    grid_y_size: int
    robots: list[RobotData]

    @classmethod
    def load_test_input(cls) -> Day14Data:
        return cls(
            grid_x_size=11,
            grid_y_size=7,
            robots=RobotData.load_all_robots_from_puzzle_input(test_input=True),
        )

    @classmethod
    def load(cls) -> Day14Data:
        return cls(
            grid_x_size=101,
            grid_y_size=103,
            robots=RobotData.load_all_robots_from_puzzle_input(),
        )


def solve(
    robots: list[RobotData],
    num_iterations: int,
    grid_x_size: int,
    grid_y_size: int,
    part_1: bool = False,
) -> bool:
    # top_left would be anything within the
    # subgrid at units
    # (0, 0) ---------------------------------------- (0, (grid_y_size / 2) - 1)
    #    |                                                |
    #    |                                                |
    #    |                                                |
    #    |                                                |
    # ((grid_x_size / 2) - 1, 0)--((grid_x_size / 2) - 1, (grid_y_size / 2) - 1)
    #
    # we could also express this as:
    #     "any cell where x is <= grid_x_size / 2 - 1 and y <= grid_y_size / 2 - 1"
    top_left = 0
    # bottom_left would be anything within the
    # subgrid at units
    # ((grid_x_size / 2) + 1, 0) -------------------------------------- ((grid_y_size / 2) + 1, (grid_y_size / 2) - 1)
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    # (grid_x_size - 1, 0)-------------------------------------------------(grid_x_size - 1, (grid_y_size / 2) - 1)
    #
    # we could also express this as:
    #     "any cell where x is >= grid_x_size / 2 + 1 and y <= grid_y_size / 2 - 1"
    bottom_left = 0
    # top_right would be anything within the
    # subgrid at units
    # (0, (grid_y_size / 2) + 1) ------------------------------------------------- (0, grid_y_size - 1)
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    # ((grid_x_size / 2 - 1), (grid_y_size / 2) + 1)--------------------((grid_x_size / 2 - 1), grid_y_size - 1)
    #
    # we could also express this as:
    #     "any cell where x is <= grid_x_size / 2 - 1 and y >= grid_y_size / 2 + 1"
    top_right = 0
    # bottom_right would be anything within the
    # subgrid at units
    # ((grid_x_size / 2) + 1, (grid_y_size / 2) + 1) -------------------------------------- ((grid_y_size / 2) + 1, grid_y_size - 1)
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    #              |                                                                       |
    # (grid_x_size - 1, (grid_y_size / 2) + 1)-------------------------------------------------(grid_x_size - 1, grid_y_size - 1)
    #
    # we could also express this as:
    #     "any cell where x is >= grid_x_size / 2 + 1 and y >= grid_y_size / 2 + 1"
    bottom_right = 0
    result_grid = [[0 for _ in range(grid_y_size)] for _ in range(grid_x_size)]
    for p, v in robots:
        # simulate where it ends up after 100 seconds.
        x, y = p
        delta_x, delta_y = v
        x = (x + (delta_x * num_iterations)) % grid_x_size
        y = (y + (delta_y * num_iterations)) % grid_y_size
        if x < 0:
            x = grid_x_size - x
        if y < 0:
            y = grid_y_size - y
        result_grid[x][y] += 1
        assert 0 <= x <= grid_x_size - 1, ValueError(str(x))
        assert 0 <= y <= grid_y_size - 1
        # check in which quadrant its final coordinates are in.
        # if it's in the "middle", ignore it.
        if x == grid_x_size // 2 or y == grid_y_size // 2:
            continue
        on_top = x <= ((grid_x_size // 2) - 1)
        on_left = y <= ((grid_y_size // 2) - 1)
        if on_top:
            if on_left:
                top_left += 1
            else:
                top_right += 1
        else:
            if on_left:
                bottom_left += 1
            else:
                bottom_right += 1
    safety_factor = reduce(mul, [top_left, top_right, bottom_left, bottom_right], 1)
    if part_1:
        print(
            f"{safety_factor=} {top_left=} {top_right=} {bottom_left=} {bottom_right=}"
        )
        return True
    else:
        for i in range(len(result_grid)):
            for j in range(len(result_grid[i])):
                if result_grid[i][j] > 1:
                    return False
        # result_grid_display = "\n".join(
        #     [
        #         "".join(
        #             [
        #                 "⬜️" if result_grid[x][y] == 0 else "⬛️"
        #                 for y in range(len(result_grid[x]))
        #             ]
        #         )
        #         for x in range(len(result_grid))
        #     ]
        # )
        # print(result_grid_display)
        return True


def part1(grid_x_size: int, grid_y_size: int, robots: list[RobotData]) -> None:
    solve(robots, 100, grid_x_size, grid_y_size, part_1=True)


def part2(grid_x_size: int, grid_y_size: int, robots: list[RobotData]) -> None:
    for i in range(grid_x_size * grid_y_size):
        if solve(robots, i, grid_x_size, grid_y_size):
            print("Seconds it takes for easter egg to appear", i)
            return

    print("No easter egg found")


if __name__ == "__main__":
    data = Day14Data.load()
    part1(*data)
    part2(*data)
