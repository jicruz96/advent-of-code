"""https://adventofcode.com/2024/day/10"""

from itertools import starmap

from rich import print

from aoc.helpers import get_input_as_grid

DAY_NUM = 10


def part1(test_input: bool = False) -> None:
    grid: list[list[int]] = [
        [int(c) for c in line]
        for line in get_input_as_grid(DAY_NUM, test_input=test_input)
    ]
    trailhead_scores: dict[tuple[int, int], int] = {}
    peak_coords: list[tuple[int, int]] = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            coords = (i, j)
            if grid[i][j] == 0:
                trailhead_scores[coords] = 0
            elif grid[i][j] == 9:
                peak_coords.append(coords)

    def find_trailheads_that_lead_to_coords(
        coords: tuple[int, int], *, seen: set[tuple[int, int]] | None = None
    ) -> list[tuple[int, int]]:
        seen = seen or set[tuple[int, int]]()
        seen.add(coords)
        val = grid[coords[0]][coords[1]]
        if val == 0:
            return [coords]
        up_coords = (coords[0] - 1, coords[1])
        down_coords = (coords[0] + 1, coords[1])
        left_coords = (coords[0], coords[1] - 1)
        right_coords = (coords[0], coords[1] + 1)
        neighbors = [up_coords, down_coords, left_coords, right_coords]
        all_trailheads: list[tuple[int, int]] = []
        for neighbor in neighbors:
            if (
                neighbor in seen
                or neighbor[0] < 0
                or neighbor[0] >= len(grid)
                or neighbor[1] < 0
                or neighbor[1] >= len(grid[neighbor[0]])
                or grid[neighbor[0]][neighbor[1]] != val - 1
            ):
                continue
            all_trailheads += find_trailheads_that_lead_to_coords(neighbor, seen=seen)
        return all_trailheads

    for coords in peak_coords:
        trailheads = find_trailheads_that_lead_to_coords(coords)
        for trailhead in trailheads:
            trailhead_scores[trailhead] += 1

    result = sum(trailhead_scores.values())
    print(f"Sum of trailhead scores: {result}")


def part2(test_input: bool = False) -> None:
    grid: list[list[int]] = [
        [int(c) for c in line]
        for line in get_input_as_grid(DAY_NUM, test_input=test_input)
    ]

    def compute_coord_rating(i: int, j: int) -> int:
        val = grid[i][j]
        if val == 9:
            return 1
        return sum(
            starmap(
                compute_coord_rating,
                [
                    (i, j)
                    for (i, j) in [
                        (i - 1, j),
                        (i + 1, j),
                        (i, j - 1),
                        (i, j + 1),
                    ]
                    if (
                        i >= 0
                        and i < len(grid)
                        and j >= 0
                        and j < len(grid[i])
                        and grid[i][j] == val + 1
                    )
                ],
            )
        )

    ratings_sum: int = sum(
        [
            compute_coord_rating(i, j) if grid[i][j] == 0 else 0
            for i in range(len(grid))
            for j in range(len(grid[i]))
        ]
    )
    print(f"Sum of ratings {ratings_sum}")


if __name__ == "__main__":
    part2(test_input=False)
