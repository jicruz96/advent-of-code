"""https://adventofcode.com/2024/day/13"""

import re
from typing import NamedTuple, Self

from aoc.helpers import get_input_text


class Machine(NamedTuple):
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int

    a_cost: int = 3
    b_cost: int = 1

    def is_valid_spot(self, coords: tuple[int, int]) -> bool:
        x, y = coords
        return x >= 0 and y >= 0 and x <= self.prize_x and y <= self.prize_y

    @classmethod
    def from_text(cls, text: str) -> Self:
        text = text.strip()
        match = re.fullmatch(
            r"""
Button A: X\+(?P<a_x>\d+), Y\+(?P<a_y>\d+)
Button B: X\+(?P<b_x>\d+), Y\+(?P<b_y>\d+)
Prize: X=(?P<prize_x>\d+), Y=(?P<prize_y>\d+)
""".strip(),
            text,
        )
        if not match:
            raise ValueError(f"Invalid game data text:\n\n{text}")
        match_dict = {k: int(v) for k, v in match.groupdict().items()}
        return cls(**match_dict)


def solve_machine(machine: Machine) -> int | None:
    """Solve for the number of A presses and B presses needed to win the
    prize on this claw machine.

    If there are no integer solutions, `None` is returned.

    Note: This function assumes that the machine has exactly one solution or
    no solutions. Infinite solutions are not supported.
    """
    a_count, remainder = divmod(
        machine.prize_x * machine.b_y - machine.prize_y * machine.b_x,
        machine.a_x * machine.b_y - machine.a_y * machine.b_x,
    )
    if remainder:
        return None
    numerator = machine.prize_x - machine.a_x * a_count
    b_count, remainder = divmod(numerator, machine.b_x)
    if remainder:
        return None
    return machine.a_cost * a_count + machine.b_cost * b_count


def part1(machines: list[Machine]) -> int:
    return sum(S for S in map(solve_machine, machines) if S is not None)


def part2(machines: list[Machine]) -> int:
    PART_2_PRIZE_OFFSET = 10_000_000_000_000
    return part1(
        [
            Machine(
                **{
                    **c._asdict(),
                    "prize_x": c.prize_x + PART_2_PRIZE_OFFSET,
                    "prize_y": c.prize_y + PART_2_PRIZE_OFFSET,
                }
            )
            for c in machines
        ]
    )


if __name__ == "__main__":
    machines = list(map(Machine.from_text, get_input_text(13).split("\n\n")))
    print("Part 1", part1(machines))
    print("Part 2", part2(machines))
