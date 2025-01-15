import functools
from typing import NamedTuple

from rich import print

from aoc.helpers import get_input_text


class Day19InputData(NamedTuple):
    available_towel_patterns: list[str]
    designs_to_display: list[str]

    @classmethod
    def load(cls, test_input: bool = False) -> "Day19InputData":
        text = get_input_text(19, test_input=test_input)
        available_towel_patterns_str, designs_to_display_str = text.split("\n\n")
        return cls(
            available_towel_patterns=available_towel_patterns_str.split(", "),
            designs_to_display=designs_to_display_str.splitlines(),
        )


def part1(test_input: bool = False) -> None:
    patterns, designs = Day19InputData.load(test_input=test_input)

    @functools.cache
    def design_is_possible(design: str) -> bool:
        if not design:
            return True
        return any(
            design.startswith(pattern) and design_is_possible(design[len(pattern) :])
            for pattern in patterns
        )

    result = sum(map(design_is_possible, designs))
    print(f"Total possible designs: {result}")


def part2(test_input: bool = False) -> None:
    patterns, designs = Day19InputData.load(test_input=test_input)

    @functools.cache
    def count_ways(design: str) -> int:
        if not design:
            return 1
        return sum(
            count_ways(design[len(pattern) :]) if design.startswith(pattern) else 0
            for pattern in patterns
        )

    result = sum(map(count_ways, designs))
    print(f"Total possible designs: {result}")


if __name__ == "__main__":
    part2(test_input=False)
