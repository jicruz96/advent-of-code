import sys
from collections import deque

from rich import print
from tqdm import tqdm

from aoc.helpers import Grid, get_input_text

sys.setrecursionlimit(5_000)


def find_shortest_path(
    grid: Grid[str], start: tuple[int, int], end: tuple[int, int]
) -> int | None:
    queue = deque[tuple[int, int, int]]([(start[0], start[1], 0)])
    seen = set[tuple[int, int]]()
    while queue:
        x, y, distance = queue.popleft()
        if x == y == len(grid) - 1:
            return distance
        for neighbor in grid.get_nondiagonal_neighbors((x, y)):
            if neighbor.value == "." and neighbor.coords not in seen:
                seen.add(neighbor.coords)
                queue.append((neighbor.i, neighbor.j, distance + 1))
    return None
    raise ValueError(f"Cannot get from {start} to {end}")


def part1(test_input: bool = False) -> None:
    coords: list[tuple[int, ...]] = [
        tuple(map(int, line.split(",")))
        for line in get_input_text(18, test_input=test_input).splitlines()
    ]
    grid_size = 71 if not test_input else 7
    grid = Grid[str].full_of(fill=".", size=grid_size)
    max_iteration = 1_024 if not test_input else 12
    for i in range(max_iteration):
        x, y = coords[i]
        grid[y][x] = "#"
    print(
        find_shortest_path(
            grid=grid,
            start=(0, 0),
            end=(grid_size - 1, grid_size - 1),
        )
    )


def part2(test_input: bool = False) -> None:
    coords: list[tuple[int, ...]] = [
        tuple(map(int, line.split(",")))
        for line in get_input_text(18, test_input=test_input).splitlines()
    ]
    # breakpoint()
    grid_size = 71 if not test_input else 7
    grid = Grid[str].full_of(fill=".", size=grid_size)
    max_iteration = 1_024 if not test_input else 12
    for i in range(max_iteration):
        x, y = coords[i]
        grid[y][x] = "#"
    for i in tqdm(list(range(max_iteration + 1, len(coords)))):
        x, y = coords[i]
        grid[y][x] = "#"
        if (
            find_shortest_path(
                grid=grid,
                start=(0, 0),
                end=(grid_size - 1, grid_size - 1),
            )
            is None
        ):
            print(f"Exit becomes inaccessible at {coords[i]}")
            break


if __name__ == "__main__":
    part2(test_input=False)
