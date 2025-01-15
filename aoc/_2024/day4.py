from typing import Iterable

from aoc.helpers import get_input_text


def find_XMAS_count_in_line(line: str) -> int:
    return line.count("XMAS") + line.count("SAMX")


def find_XMAS_count_in_lines(lines: Iterable[str]) -> int:
    return sum(map(find_XMAS_count_in_line, lines))


def find_XMAS_count_in_horizontal_lines(text: str) -> int:
    return find_XMAS_count_in_lines(text.splitlines())


def find_XMAS_count_in_vertical_lines(text: str) -> int:
    lines_by_index: dict[int, str] = {}
    for line in text.splitlines():
        for i, char in enumerate(line):
            if i not in lines_by_index:
                lines_by_index[i] = ""
            lines_by_index[i] += char
    return find_XMAS_count_in_lines(lines_by_index.values())


def find_left_to_right_diagonal_lines_in_2d_grid_text(text: str) -> list[str]:
    lines_by_diagonal_id: dict[int, str] = {}
    for i, line in enumerate(text.splitlines()):
        for j, char in enumerate(line):
            diagonal_id = i - j
            if diagonal_id not in lines_by_diagonal_id:
                lines_by_diagonal_id[diagonal_id] = ""
            lines_by_diagonal_id[diagonal_id] += char
    return list(lines_by_diagonal_id.values())


def find_XMAS_count_in_diagonal_lines(text: str) -> int:
    reversed_text = "\n".join(["".join(reversed(line)) for line in text.splitlines()])
    lines = find_left_to_right_diagonal_lines_in_2d_grid_text(
        text
    ) + find_left_to_right_diagonal_lines_in_2d_grid_text(reversed_text)
    return find_XMAS_count_in_lines(lines)


def part1(test_input: bool = False):
    text = get_input_text(4, test_input=test_input)
    horizontal_count = find_XMAS_count_in_horizontal_lines(text)
    vertical_count = find_XMAS_count_in_vertical_lines(text)
    diagonal_count = find_XMAS_count_in_diagonal_lines(text)
    count = horizontal_count + vertical_count + diagonal_count
    print("XMAS count:", count)


def part2(test_input: bool = False):
    text = get_input_text(4, test_input=test_input)
    lines = text.splitlines()
    count = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != "A":
                continue
            if i == 0 or i == len(lines) - 1:
                continue
            if j == 0 or j == len(line) - 1:
                continue
            top_left = lines[i - 1][j - 1]
            top_right = lines[i - 1][j + 1]
            bottom_left = lines[i + 1][j - 1]
            bottom_right = lines[i + 1][j + 1]
            corners = [
                top_left,
                top_right,
                bottom_left,
                bottom_right,
            ]
            if corners.count("M") != 2:
                continue
            if corners.count("S") != 2:
                continue
            if top_right != top_left and top_right != bottom_right:
                continue
            count += 1
    print("X-MAS count", count)


if __name__ == "__main__":
    print("PART 1")
    part1(test_input=True)
    part1()
    print("PART 2")
    part2(test_input=True)
    part2()
