"""https://adventofcode.com/2024/day/13"""

import re
from typing import NamedTuple

from rich import print

from aoc.helpers import get_input_text

game_data_pattern = re.compile(
    r"""
Button A: X\+(?P<a_x>\d+), Y\+(?P<a_y>\d+)
Button B: X\+(?P<b_x>\d+), Y\+(?P<b_y>\d+)
Prize: X=(?P<prize_x>\d+), Y=(?P<prize_y>\d+)
""".strip(),
    re.MULTILINE,
)


class GameConfig(NamedTuple):
    a_x: int  # 3 tokens required for a A move
    a_y: int
    b_x: int  # 1 token required for a B move
    b_y: int
    prize_x: int
    prize_y: int

    @classmethod
    def from_text(cls, text: str) -> "GameConfig":
        text = text.strip()
        match = re.fullmatch(game_data_pattern, text)
        if not match:
            raise ValueError(f"Invalid game data text:\n\n{text}")
        match_dict = {k: int(v) for k, v in match.groupdict().items()}
        return cls(**match_dict)


def solve_game(config: GameConfig) -> int | None:
    """
    Determine the minimum cost to align the claw with the prize for a given machine configuration.

    The claw moves along the X and Y axes according to the following rules:
      - Button A moves the claw by `a_x` units along the X-axis and `a_y` units along the Y-axis.
      - Button B moves the claw by `b_x` units along the X-axis and `b_y` units along the Y-axis.
      - The claw starts at (0, 0) and needs to reach (prize_x, prize_y).

    The cost of pressing a button is:
      - Button A: 3 tokens per press.
      - Button B: 1 token per press.

    This function solves the system of equations:
      - A_count * a_x + B_count * b_x = prize_x
      - A_count * a_y + B_count * b_y = prize_y
    to find nonnegative integers `A_count` and `B_count` that satisfy both equations.

    If such a solution exists, the function returns the minimal cost:
      cost = 3 * A_count + 1 * B_count.
    If no solution exists, it returns None.

    Args:
        config (GameConfig): Configuration for the claw machine.

    Returns:
        Optional[int]: The minimal cost if a solution exists, or None if it doesn't.
    """

    # Extract values for clarity
    a_x_move, a_y_move, b_x_move, b_y_move, target_x, target_y = config
    determinant = a_x_move * b_y_move - a_y_move * b_x_move
    if determinant == 0:
        return solve_degenerate_case(
            a_x_move, a_y_move, b_x_move, b_y_move, target_x, target_y
        )
    # Solve for the number of presses using Cramer's rule
    # https://en.wikipedia.org/wiki/Cramer%27s_rule
    a_count_numerator = target_x * b_y_move - target_y * b_x_move
    b_count_numerator = -target_x * a_y_move + target_y * a_x_move

    if a_count_numerator % determinant != 0 or b_count_numerator % determinant != 0:
        # If the solution is not an integer, it's invalid
        return None

    a_cost = 3
    b_cost = 1
    a_count = a_count_numerator // determinant
    b_count = b_count_numerator // determinant

    # Check if the solution is valid (nonnegative)
    if a_count < 0 or b_count < 0:
        return None

    return a_cost * a_count + b_cost * b_count


def solve_degenerate_case(
    move_x_a: int,
    move_y_a: int,
    move_x_b: int,
    move_y_b: int,
    target_x: int,
    target_y: int,
) -> int | None:
    """
    Handle cases where the determinant is zero, indicating that Buttons A and B
    do not produce independent movement.

    In these cases, only one button may be sufficient to align the claw with the prize.
    This function checks if the claw can reach the prize using only Button A or Button B.

    Args:
        move_x_a, move_y_a (int): Button A increments.
        move_x_b, move_y_b (int): Button B increments.
        target_x, target_y (int): Prize coordinates.

    Returns:
        int | None: The minimal cost if a solution exists, or None if it doesn't.
    """

    def check_b():
        if move_x_b != 0 and target_x % move_x_b == 0:
            b_count = target_x // move_x_b
            if b_count * move_y_b == target_y:
                return 1 * b_count  # Cost is only presses of Button B
        if move_y_b != 0 and target_y % move_y_b == 0:
            b_count = target_y // move_y_b
            if b_count * move_x_b == target_x:
                return 1 * b_count  # Cost is only presses of Button B
        return None

    def check_a():
        if move_x_a != 0 and target_x % move_x_a == 0:
            a_count = target_x // move_x_a
            if a_count * move_y_a == target_y:
                return 3 * a_count  # Cost is 3 tokens per Button A press
        if move_y_a != 0 and target_y % move_y_a == 0:
            a_count = target_y // move_y_a
            if a_count * move_x_a == target_x:
                return 3 * a_count  # Cost is 3 tokens per Button A press
        return None

    # Case 1: Button A is zero'd out
    if move_x_a == 0 and move_y_a == 0:
        return check_b()

    # Case 2: Button B is zero'd out
    if move_x_b == 0 and move_y_b == 0:
        return check_a()

    a_cost = check_a()
    b_cost = check_b()
    if a_cost is None:
        return b_cost
    if b_cost is None:
        return a_cost
    return min(a_cost, b_cost)


def solve(games: list[GameConfig]) -> int:
    """
    Given a list of GameConfig objects, determine the sum of minimal costs
    for all solvable configurations.

    Returns the total minimal cost.
    """
    return sum([res for res in map(solve_game, games) if res is not None])


if __name__ == "__main__":
    # Get input from Advent of Code
    text = get_input_text(13, test_input=False)
    configs = list(map(GameConfig.from_text, text.split("\n\n")))
    PART_2_PRIZE_OFFSET = 10_000_000_000_000
    part2_configs = [
        GameConfig(
            a_x=c.a_x,
            a_y=c.a_y,
            b_x=c.b_x,
            b_y=c.b_y,
            prize_x=c.prize_x + PART_2_PRIZE_OFFSET,
            prize_y=c.prize_y + PART_2_PRIZE_OFFSET,
        )
        for c in configs
    ]
    print("[bold]Part 1 total cost[/bold]:", solve(configs))
    print("[bold]Part 2 total cost[/bold]:", solve(part2_configs))
    # print("[bold green] numpy_solution Part 2 total cost[/bold green]:", solve(part2_configs))
