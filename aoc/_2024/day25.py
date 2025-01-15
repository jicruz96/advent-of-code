import itertools

from rich import print

from aoc.helpers import Grid, get_input_text


def compute_lock_pin_heights(lock_grid: Grid[str]) -> list[int]:
    pin_heights = [0] * len(lock_grid[0])
    for i in range(len(lock_grid[0])):
        for j in range(len(lock_grid)):
            if lock_grid[j][i] != "#":
                pin_heights[i] = j
                break
    return pin_heights


def compute_key__pin_heights(key_grid: Grid[str]) -> list[int]:
    pin_heights = [0] * len(key_grid[0])
    for i in range(len(key_grid[0])):
        for j in range(len(key_grid) - 1, -1, -1):
            if key_grid[j][i] != "#":
                pin_heights[i] = len(key_grid) - 1 - j
                break
    return pin_heights


def lock_key_fits(
    lock_pin_height: list[int],
    key_pin_height: list[int],
    max_height: int,
) -> bool:
    assert len(lock_pin_height) == len(key_pin_height)
    for i in range(len(lock_pin_height)):
        overlaps = (lock_pin_height[i] + key_pin_height[i]) > max_height
        if overlaps:
            return False
    # print(f"{lock_pin_height=} and {key_pin_height=} fit!")
    return True


def part1():
    text = get_input_text(25, test_input=False)

    locks: list[Grid[str]] = []
    keys: list[Grid[str]] = []

    for grid_text in text.split("\n\n"):
        grid = Grid.from_string(grid_text)
        if grid[0][0] == "#":
            locks.append(Grid(grid[1:]))
        else:
            keys.append(Grid(grid[:-1]))

    lock_pin_heights: list[list[int]] = list(map(compute_lock_pin_heights, locks))
    key__pin_heights: list[list[int]] = list(map(compute_key__pin_heights, keys))

    unique_fits: list[tuple[list[int], list[int]]] = []
    for lock_pin_height, key_pin_height in itertools.product(
        lock_pin_heights, key__pin_heights
    ):
        if lock_key_fits(lock_pin_height, key_pin_height, len(locks[0]) - 1):
            unique_fits.append((lock_pin_height, key_pin_height))

    print(f"{len(unique_fits)=}")


def part2():
    """Oh! There is no Part 2!"""


if __name__ == "__main__":
    part1()
