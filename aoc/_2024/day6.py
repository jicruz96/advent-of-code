from rich import print
from tqdm import tqdm

from aoc.helpers import get_input_text


def part1(test_input: bool = False) -> None:
    text = get_input_text(6, test_input=test_input)

    # convert input into grid
    grid: list[list[str]] = []
    for line in text.splitlines():
        grid.append(list(line))

    # find the start position of the guard
    start_pos: tuple[int, int] = (-1, -1)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "^":
                start_pos = (i, j)

    if start_pos == (-1, -1):
        raise RuntimeError("Invalid input does not contain a start position")

    # traverse grid
    #    * making sure to count unique positions
    unique_positions: set[tuple[int, int]] = set()
    # keep checking as long as current position is within grid
    i, j = start_pos
    direction_dictionary = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}
    while True:
        unique_positions.add((i, j))
        # traverse!
        delta_i, delta_j = direction_dictionary[grid[i][j]]
        new_i, new_j = (i + delta_i), (j + delta_j)
        if not (
            new_i >= 0 and new_i < len(grid) and new_j >= 0 and new_j < len(grid[new_i])
        ):
            break
        if grid[new_i][new_j] == "#":
            # rotate 90 degrees to the right
            match grid[i][j]:
                case "^":
                    grid[i][j] = ">"
                case ">":
                    grid[i][j] = "v"
                case "v":
                    grid[i][j] = "<"
                case "<":
                    grid[i][j] = "^"
                case _:
                    print("This should have never happened!")
                    breakpoint()
                    raise RuntimeError
        else:
            grid[new_i][new_j] = grid[i][j]
            grid[i][j] = "."
            i = new_i
            j = new_j

    count: int = len(unique_positions)
    print(f"Unique positions traversed by guard {count}")


def _is_stuck_in_a_loop(grid: list[list[str]]) -> bool:
    # find the start position of the guard
    start_pos: tuple[int, int] = (-1, -1)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] in ("^", ">", "<", "v"):
                start_pos = (i, j)
                break

    grid = [[char for char in line] for line in grid]

    if start_pos == (-1, -1):
        print(grid)
        raise RuntimeError("Invalid input does not contain a start position")

    # traverse grid
    #    * making sure to count unique positions
    unique_positions: set[tuple[int, int]] = set()
    unique_positions_with_direction: set[tuple[int, int, str]] = set()
    # keep checking as long as current position is within grid
    i, j = start_pos
    direction_dictionary = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}
    while True:
        unique_positions.add((i, j))
        # traverse!
        direction = grid[i][j]
        delta_i, delta_j = direction_dictionary[direction]
        if (i, j, direction) in unique_positions_with_direction:
            # breakpoint()
            return True
        unique_positions_with_direction.add((i, j, direction))
        new_i, new_j = (i + delta_i), (j + delta_j)
        if not (
            new_i >= 0 and new_i < len(grid) and new_j >= 0 and new_j < len(grid[new_i])
        ):
            break
        if grid[new_i][new_j] == "#":
            # rotate 90 degrees to the right
            match grid[i][j]:
                case "^":
                    grid[i][j] = ">"
                case ">":
                    grid[i][j] = "v"
                case "v":
                    grid[i][j] = "<"
                case "<":
                    grid[i][j] = "^"
                case _:
                    print("This should have never happened!")
                    breakpoint()
                    raise RuntimeError
        else:
            grid[new_i][new_j] = grid[i][j]
            grid[i][j] = "."
            i = new_i
            j = new_j
        # print(grid)
    # breakpoint()
    return False


def part2(test_input: bool = False) -> None:
    text = get_input_text(6, test_input=test_input)

    # convert input into grid
    grid: list[list[str]] = []
    for line in text.splitlines():
        grid.append(list(line))

    result = _is_stuck_in_a_loop(grid)
    possible_spots: int = 0
    coords = [(i, j) for i in range(len(grid)) for j in range(len(grid[i]))]
    for i, j in tqdm(coords):
        if grid[i][j] != ".":
            continue
        grid[i][j] = "#"
        result = _is_stuck_in_a_loop(grid)
        if result is True:
            possible_spots += 1
        grid[i][j] = "."
    print(f"Possible spots to force a loop: {possible_spots}")


if __name__ == "__main__":
    part2(test_input=False)
