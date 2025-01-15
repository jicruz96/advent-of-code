from __future__ import annotations

import os

INPUTS_FOLDER = "inputs"


def _get_input_filename(day: int, year: int, test_input: bool = False) -> str:
    if test_input:
        return os.path.join(INPUTS_FOLDER, str(year), f"day{day}-test.txt")
    return os.path.join(INPUTS_FOLDER, str(year), f"day{day}.txt")


def get_input_text(day: int, year: int = 2024, test_input: bool = False) -> str:
    with open(_get_input_filename(day, year, test_input), "r") as fp:
        return fp.read()


def get_input_as_grid(
    day: int, year: int = 2024, test_input: bool = False
) -> list[list[str]]:
    text = get_input_text(day, year, test_input)
    return [[char for char in line] for line in text.splitlines()]
