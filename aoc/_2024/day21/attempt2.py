import functools
import itertools
from collections import deque
from typing import Callable, Literal, Sequence, TypeAlias, cast

from rich import print

from aoc.helpers import Cell, Grid, get_input_text

DirectionalKey: TypeAlias = Literal["^", "<", "v", ">", "A", " "]
NumericKey: TypeAlias = Literal[
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", " "
]
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


def default_scorer(src: tuple[Cell, int], dest: tuple[Cell, int | None]):
    _, src_score = src
    __, dest_score = dest
    move_score = 1 + src_score
    if dest_score is None or move_score < dest_score:
        return move_score
    return dest_score


def default_score_init(grid: Grid[str], start_pos: Cell[str]):
    scores = Grid[int | None].full_of(
        fill=None,
        size=len(grid),
    )
    scores[start_pos.i][start_pos.j] = 0
    return scores


def solve[ScoreType](
    maze: Grid[str],
    start: str = "S",
    end: str = "E",
    unsafe: Sequence[str] = ("#",),
    scorer: Callable[
        [tuple[Cell, ScoreType], tuple[Cell, ScoreType]], ScoreType
    ] = default_scorer,
    score_init: Callable[[Grid[str], Cell[str]], Grid[ScoreType]] = default_score_init,
) -> ScoreType:
    start_pos = maze.first(start, strict=True)
    scores = score_init(maze, start_pos)
    queue = deque[Cell]([start_pos])

    def move_and_update_score(curr: Cell, next_coords: tuple[int, int]) -> None:
        if (
            (next := maze.at(next_coords))
            and next.value != start
            and next.value not in unsafe
        ):
            curr_score = scores.at(curr.coords, strict=True).value
            next_score = scores.at(next.coords, strict=True).value
            new_score = scorer((curr, curr_score), (next, next_score))
            scores[next.i][next.j] = new_score
            if new_score != next_score:
                queue.append(next)

    while queue:
        pos = queue.popleft()
        move_and_update_score(pos, pos.up_coords)
        move_and_update_score(pos, pos.down_coords)
        move_and_update_score(pos, pos.right_coords)
        move_and_update_score(pos, pos.left_coords)
    end_score = scores.at(maze.first(end, strict=True).coords, strict=True).value
    return end_score


def part1(test_input: bool = False) -> None:
    codes = get_input_text(21, test_input=test_input).splitlines()
    # codes = codes[:1]
    complexity_sum = sum(map(get_code_complexity, codes))
    print(f"{complexity_sum=}")


def score_init(grid: Grid[str], _: Cell[str]) -> Grid[str]:
    return Grid[str].full_of(fill="", size=grid.size)


def get_direction_to_get_to_neighbor(cell: Cell, neighbor: Cell) -> DirectionalKey:
    match cell.neighbor_type(neighbor, strict=True):
        case "top":
            return "^"
        case "bottom":
            return "v"
        case "left":
            return "<"
        case "right":
            return ">"


def scorer(curr: tuple[Cell, str], next: tuple[Cell, str]) -> str:
    new_path = curr[1] + get_direction_to_get_to_neighbor(curr[0], next[0])
    if len(next[1]) == 0:
        return new_path
    if len(next[1]) < len(new_path):
        return next[1]
    # if they're the same length, return path
    # with fewer changes.
    if len(new_path) < len(next[1]):
        return new_path
    changed = 0
    changed_new = 0
    for i in range(1, len(new_path)):
        changed += next[1][i - 1] != next[1][i]
        changed_new += new_path[i - 1] != new_path[i]
    if changed > changed_new:
        return new_path
    return next[1]


def scorer2(curr: tuple[Cell, str], next: tuple[Cell, str]) -> str:
    new_path = curr[1] + directional_keypad_solve(
        start=get_current_direction_from_path(curr[1]),
        end=get_direction_to_get_to_neighbor(curr[0], next[0]),
    )
    if len(next[1]) == 0:
        return new_path
    if len(next[1]) < len(new_path):
        return next[1]
    # if they're the same length, return path
    # with fewer changes.
    if len(new_path) < len(next[1]):
        return new_path
    changed = 0
    changed_new = 0
    for i in range(1, len(new_path)):
        changed += next[1][i - 1] != next[1][i]
        changed_new += new_path[i - 1] != new_path[i]
    if changed > changed_new:
        return new_path
    return next[1]


@functools.cache
def directional_keypad_solve(start: DirectionalKey, end: DirectionalKey) -> str:
    return (
        solve(
            maze=DIRECTIONAL_KEYPAD,
            start=start,
            end=end,
            unsafe=(" ",),
            score_init=score_init,
            scorer=scorer,
        )
        + "A"
    )


@functools.cache
def directional_keypad_solve2(start: DirectionalKey, end: DirectionalKey) -> str:
    move_to_direction_path = solve(
        maze=DIRECTIONAL_KEYPAD,
        start=start,
        end=end,
        unsafe=(" ",),
        score_init=score_init,
        scorer=scorer2,
    )
    press_direction_path = directional_keypad_solve(
        get_current_direction_from_path(move_to_direction_path),
        end,
    )
    return move_to_direction_path + press_direction_path


def get_current_direction_from_path(score: str) -> DirectionalKey:
    direction = score[-1] if score else "A"
    return cast(DirectionalKey, direction)


def numeric_scorer(
    curr: tuple[Cell, str],
    next: tuple[Cell, str],
) -> str:
    go_to_direction = directional_keypad_solve2(
        start=get_current_direction_from_path(curr[1]),
        end=get_direction_to_get_to_neighbor(curr[0], next[0]),
    )
    new_potential_path = curr[1] + go_to_direction
    if 0 < len(next[1]) < len(new_potential_path):
        return next[1]
    return new_potential_path


@functools.cache
def numeric_keypad_solve(start: NumericKey, end: NumericKey) -> str:
    move_to_number_path = solve(
        maze=NUMERIC_KEYPAD,
        start=start,
        end=end,
        unsafe=" ",
        score_init=score_init,
        scorer=numeric_scorer,
    )
    press_number_path = directional_keypad_solve2(
        start=get_current_direction_from_path(move_to_number_path),
        end="A",
    )
    return move_to_number_path + press_number_path


def get_code_complexity(code: str) -> int:
    assert code[-1] == "A"
    code_sequence: str = ""
    for start, end in itertools.pairwise("A" + code):
        code_sequence += numeric_keypad_solve(start, end)
    numeric_part_of_code = int(code[:-1])
    complexity = len(code_sequence) * numeric_part_of_code
    print(
        f"{code!r}: [{len(code_sequence)}] {code_sequence} "
        f"complexity: {len(code_sequence)} * {numeric_part_of_code} = {complexity}"
    )
    return complexity


if __name__ == "__main__":
    part1(test_input=True)
