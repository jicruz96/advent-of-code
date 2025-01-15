import itertools

from aoc.helpers import get_input_text


def _check_if_levels_is_safe(levels: list[int]) -> bool:
    expect_ascending: bool = levels[0] < levels[1]
    for previous_level, current_level in itertools.pairwise(levels):
        if expect_ascending:
            if current_level < previous_level:
                return False
        else:
            if current_level > previous_level:
                return False
        distance = abs(current_level - previous_level)
        if distance > 3 or distance < 1:
            return False
    return True


def part1() -> None:
    lines = get_input_text(2).splitlines()
    total_safe_reports: int = 0
    for report in lines:
        levels = [int(level_str) for level_str in report.split()]
        is_safe = _check_if_levels_is_safe(levels)
        if is_safe:
            total_safe_reports += 1
        print(report, f"-> {'SAFE' if is_safe else 'UNSAFE'}")
    print(f"Total safe reports: {total_safe_reports}/{len(lines)}")


def part2() -> None:
    lines = get_input_text(
        2,
        # test_input=True,
    ).splitlines()
    total_safe_reports: int = 0
    for report in lines:
        levels = [int(level_str) for level_str in report.split()]
        is_safe = _check_if_levels_is_safe(levels)
        if is_safe:
            total_safe_reports += 1
        else:
            # brute force it!
            for j in range(len(levels)):
                levels_copy_excluding_j = levels[:j] + levels[j + 1 :]
                is_safe = _check_if_levels_is_safe(levels_copy_excluding_j)
                if is_safe:
                    total_safe_reports += 1
                    break

        print(report, f"-> {'SAFE' if is_safe else 'UNSAFE'}")
    print(f"Total safe reports: {total_safe_reports}/{len(lines)}")


if __name__ == "__main__":
    part1()
    part2()
