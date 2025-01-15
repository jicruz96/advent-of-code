import re

from aoc.helpers import get_input_text


def part1() -> None:
    text = get_input_text(3)

    # find all instances of the pattern:
    # mul(<some 1 to 3-digit number>, <some 1 to 3-digit number>)
    total: int = 0
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    for n1_str, n2_str in re.findall(pattern, text):
        total += int(n1_str) * int(n2_str)
    print(f"Total muls: {total}")


def part2(test_input: bool = False) -> None:
    text = get_input_text(3, test_input=test_input)
    print(text)

    # find all instances of the pattern:
    # mul(<some 1 to 3-digit number>, <some 1 to 3-digit number>)
    total: int = 0
    do_dont_pattern = re.compile(r"do(n't)?\(\)")
    new_string = ""
    do = True
    tmp_text = text
    while match := re.search(do_dont_pattern, tmp_text):
        i, j = match.span()
        if do:
            substring = tmp_text[:i]
            print(f"appending {substring!r}")
            new_string += substring
        do = match.groups()[0] is None
        # print("index is", j)
        tmp_text = tmp_text[j:]
    if do and tmp_text:
        substring = tmp_text
        # print(f"appending {substring!r}")
        new_string += substring
    print("new_string is", new_string)
    text = new_string
    total: int = 0
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    for n1_str, n2_str in re.findall(pattern, text):
        mul = int(n1_str) * int(n2_str)
        print(f"{n1_str} * {n2_str} = {mul}")
        total += mul
    print(f"Total muls: {total}")


if __name__ == "__main__":
    part1()
    part2(test_input=False)
