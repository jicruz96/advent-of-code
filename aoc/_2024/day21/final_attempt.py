import functools
import itertools

from aoc.helpers import Grid, get_input_text

NUMERIC_KEYPAD = Grid(
    [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"],
    ]
)
DIRECTIONAL_KEYPAD = Grid(
    [
        [" ", "^", "A"],
        ["<", "v", ">"],
    ]
)


@functools.cache
def find_paths(grid: Grid[str], start: str, end: str) -> list[str]:
    queue = [(grid.first(start, strict=True).coords, "")]
    space_pos = grid.first(" ", strict=True).coords
    end_i, end_j = end_pos = grid.first(end, strict=True).coords
    paths: list[str] = []
    while queue:
        pos, path = queue.pop()
        if pos == end_pos:
            paths.append(path + "A")
            continue
        i, j = pos
        if j != end_j:
            if j < end_j:
                new_j_pos = (i, j + 1)
                move = ">"
            else:
                new_j_pos = (i, j - 1)
                move = "<"
            if new_j_pos != space_pos:
                queue.append((new_j_pos, path + move))
        if i != end_i:
            if i < end_i:
                new_i_pos = (i + 1, j)
                move = "v"
            else:
                new_i_pos = (i - 1, j)
                move = "^"
            if new_i_pos != space_pos:
                queue.append((new_i_pos, path + move))
    return paths


@functools.cache
def get_shortest_path(keypad: Grid[str], start: str, end: str, depth: int):
    return min(
        get_shortest_code_sequence_length(DIRECTIONAL_KEYPAD, sequence, depth - 1)
        for sequence in find_paths(keypad, start, end)
    )


@functools.cache
def get_shortest_code_sequence_length(keypad: Grid[str], code: str, depth: int) -> int:
    if depth == 0:
        return len(code)

    return sum(
        itertools.starmap(
            lambda start, end: get_shortest_path(keypad, start, end, depth),
            itertools.pairwise("A" + code),
        )
    )


def get_code_complexity(code: str, depth: int) -> int:
    return get_shortest_code_sequence_length(NUMERIC_KEYPAD, code, depth) * int(
        code[:-1]
    )


def part1():
    return solve(3)


def part2():
    return solve(26)


def solve(depth: int) -> int:
    codes = get_input_text(21).splitlines()
    return sum(map(lambda code: get_code_complexity(code, depth), codes))


if __name__ == "__main__":
    print(part1())
    print(part2())
