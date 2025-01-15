from typing import Literal, TypeAlias

from rich import print

from aoc.helpers import Grid, get_input_text

vibes = """
Numerical keypad:
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

Directional keypad:
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
NumericKey: TypeAlias = Literal[
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", " "
]
DirectionalKey: TypeAlias = Literal["^", "<", "v", ">", "A", " "]


numerical_keypad = Grid[NumericKey](
    [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"],
    ]
)
directional_keypad = Grid[DirectionalKey](
    [
        [" ", "^", "A"],
        ["<", "v", ">"],
    ]
)

bazinga: dict[NumericKey, dict[NumericKey, list[DirectionalKey]]] = {
    "0": {
        "A": [">"],
        "0": [],
        "1": ["^", "<"],
        "2": ["^"],
        "3": ["^", ">"],
        "4": ["^", "^", "<"],
        "5": ["^", "^"],
        "6": ["^", "^", ">"],
        "7": ["^", "^", "^", "<"],
        "8": ["^", "^", "^"],
        "9": ["^", "^", "^", ">"],
    },
    "1": {
        "A": [">", ">", "v"],
        "0": [">", "v"],
        "1": [],
        "2": [">"],
        "3": [">", ">"],
        "4": ["^"],
        "5": ["^", ">"],
        "6": ["^", ">", ">"],
        "7": ["^", "^"],
        "8": ["^", "^", ">"],
        "9": ["^", "^", ">", ">"],
    },
    "2": {
        "A": [">", "v"],
        "0": ["v"],
        "1": ["<"],
        "2": [],
        "3": [">"],
        "4": ["^", "<"],
        "5": ["^"],
        "6": ["^", ">"],
        "7": ["^", "^", "<"],
        "8": ["^", "^"],
        "9": ["^", "^", ">"],
    },
    "3": {
        "A": ["v"],
        "0": ["v", "<"],
        "1": ["<", "<"],
        "2": ["<"],
        "3": [],
        "4": ["^", "<", "<"],
        "5": ["^", "<"],
        "6": ["^"],
        "7": ["^", "^", "<", "<"],
        "8": ["^", "^", "<"],
        "9": ["^", "^"],
    },
    "4": {
        "A": [">", ">", "v", "v"],
        "0": [">", "v", "v"],
        "1": ["v"],
        "2": [">", "v"],
        "3": [">", ">", "v"],
        "4": [],
        "5": [">"],
        "6": [">", ">"],
        "7": ["^"],
        "8": ["^", ">"],
        "9": ["^", ">", ">"],
    },
    "5": {
        "A": [">", "v", "v"],
        "0": ["v", "v"],
        "1": ["v", "<"],
        "2": ["v"],
        "3": [">", "v"],
        "4": ["<"],
        "5": [],
        "6": [">"],
        "7": ["^", "<"],
        "8": ["^"],
        "9": ["^", ">"],
    },
    "6": {
        "A": ["v", "v"],
        "0": ["v", "v", "<"],
        "1": ["v", "<", "<"],
        "2": ["v", "<"],
        "3": ["v"],
        "4": ["<", "<"],
        "5": ["<"],
        "6": [],
        "7": ["^", "<", "<"],
        "8": ["^", "<"],
        "9": ["^"],
    },
    "7": {
        "A": [">", ">", "v", "v", "v"],
        "0": [">", "v", "v", "v"],
        "1": ["v", "v"],
        "2": [">", "v", "v"],
        "3": [">", ">", "v", "v"],
        "4": ["v"],
        "5": [">", "v"],
        "6": [">", ">", "v"],
        "7": [],
        "8": [">"],
        "9": [">", ">"],
    },
    "8": {
        "A": [">", "v", "v", "v"],
        "0": ["v", "v", "v"],
        "1": ["v", "v", "<"],
        "2": ["v", "v"],
        "3": [">", "v", "v"],
        "4": ["v", "<"],
        "5": ["v"],
        "6": [">", "v"],
        "7": ["<"],
        "8": [],
        "9": [">"],
    },
    "9": {
        "A": ["v", "v", "v"],
        "0": ["v", "v", "v", "<"],
        "1": ["v", "v", "<", "<"],
        "2": ["v", "v", "<"],
        "3": ["v", "v"],
        "4": ["v", "<", "<"],
        "5": ["v", "<"],
        "6": ["v"],
        "7": ["<", "<"],
        "8": ["<"],
        "9": [],
    },
    "A": {
        "A": [],
        "0": ["<"],
        "1": ["^", "<", "<"],
        "2": ["^", "<"],
        "3": ["^"],
        "4": ["^", "^", "<", "<"],
        "5": ["^", "^", "<"],
        "6": ["^", "^"],
        "7": ["^", "^", "^", "<", "<"],
        "8": ["^", "^", "^", "<"],
        "9": ["^", "^", "^"],
    },
}

swahili: dict[DirectionalKey, dict[DirectionalKey, list[DirectionalKey]]] = {
    "^": {
        "^": [],
        "v": ["v"],
        "<": ["v", "<"],
        ">": [">", "v"],
        "A": [">"],
    },
    "v": {
        "^": ["^"],
        "v": [],
        "<": ["<"],
        ">": [">"],
        "A": ["^", ">"],
    },
    "<": {
        "^": ["^", ">"],
        "v": [">"],
        "<": [],
        ">": [">", ">"],
        "A": ["^", ">", ">"],
    },
    ">": {
        "^": ["^", "<"],
        "v": ["<"],
        "<": ["<", "<"],
        ">": [],
        "A": ["^"],
    },
    "A": {
        "^": ["<"],
        "v": ["v", "<"],
        "<": ["v", "<", "<"],
        ">": ["v"],
        "A": [],
    },
}


def compile_code_sequence(code: str) -> list[DirectionalKey]:
    directions_for_2nd_robot = numeric_to_directional(code, debug=code == "379A")
    directions_for_third_robot = directional_to_directional(
        directions_for_2nd_robot, debug=code == "379A"
    )
    my_directions = directional_to_directional(directions_for_third_robot, debug=True)
    print(
        f"\n----\n"
        f"   {''.join(my_directions)}\n"
        f"   {''.join(directions_for_third_robot)}\n"
        f"   {''.join(directions_for_2nd_robot)}\n"
        f"   {code}\n\n"
    )
    return my_directions


def directional_to_directional(
    code: list[DirectionalKey],
    d: dict[DirectionalKey, dict[DirectionalKey, list[DirectionalKey]]] = swahili,
    debug: bool = False,
) -> list[DirectionalKey]:
    i = 0
    directions: list[DirectionalKey] = []
    # we always start at A
    prefix: list[DirectionalKey] = ["A"]
    code = prefix + code
    if debug:
        print(f"\n-----directional debug for code={''.join(code)}-------\n")
    while i < len(code) - 1:
        src = code[i]
        dest = code[i + 1]
        directions.extend(d[src][dest])  # type: ignore
        directions.append("A")
        if debug:
            print(f"{src=} {dest=} direction={''.join(d[src][dest])}A")
        i += 1
    return directions


def numeric_to_directional(code: str, debug: bool = False) -> list[DirectionalKey]:
    assert code[-1] == "A"
    i = 0
    directions: list[DirectionalKey] = []
    # we always start at A
    code = "A" + str(code)
    if debug:
        print(f"\n-----numeric debug for {code=}-------\n")
    while i < len(code) - 1:
        src = code[i]
        dest = code[i + 1]
        directions.extend(bazinga[src][dest])  # type: ignore
        directions.append("A")
        if debug:
            print(f"{src=} {dest=} direction={''.join(bazinga[src][dest])}A")
        i += 1
    return directions


def get_code_complexity(code: str) -> int:
    assert code[-1] == "A"
    code_sequence = "".join(compile_code_sequence(code))  # type: ignore
    numeric_part_of_code = int(code[:-1])
    complexity = len(code_sequence) * numeric_part_of_code
    print(
        f"{code=} {code_sequence=} {len(code_sequence)=} {numeric_part_of_code=} {complexity=}"
    )
    return complexity


def part1(test_input: bool = False) -> None:
    text = get_input_text(21, test_input=test_input)

    codes = text.splitlines()

    complexity_sum = sum(map(get_code_complexity, codes))
    print(f"{complexity_sum=}")
    print(vibes)


if __name__ == "__main__":
    part1(test_input=True)
