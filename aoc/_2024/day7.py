from rich import print

from aoc.helpers import get_input_text


def does_nums_add_up_to_n(nums: list[int], n: float) -> bool:
    if not nums:
        return False
    if len(nums) == 1:
        return nums[0] == n
    if len(nums) == 2:
        return (nums[0] + nums[1] == n) or (nums[0] * nums[1] == n)
    n_minus_last_num = n - nums[-1]
    if does_nums_add_up_to_n(nums[:-1], n_minus_last_num):
        return True
    n_divided_by_last_num = n / nums[-1]
    if does_nums_add_up_to_n(nums[:-1], n_divided_by_last_num):
        return True
    return False


def assert_float_is_just_int(x: float, debug: bool) -> bool:
    if x - int(x) != 0:
        if debug:
            # print(f"{x!r} is not an int")
            # breakpoint()
            pass
        return False
    return True


def _concat_nums(a: float, b: float, *, debug: bool = False) -> int:
    assert_float_is_just_int(a, debug=debug)
    assert_float_is_just_int(b, debug=debug)
    return int(str(int(a)) + str(int(b)))


def does_nums_add_up_to_n_part2(nums: list[int], n: float) -> bool:
    if not nums:
        return False
    if len(nums) == 1:
        return nums[0] == n
    if len(nums) == 2:
        return (
            (nums[0] + nums[1] == n)
            or (nums[0] * nums[1] == n)
            or (_concat_nums(nums[0], nums[1]) == n)
        )
    n_minus_last_num = n - nums[-1]
    if does_nums_add_up_to_n_part2(nums[:-1], n_minus_last_num):
        return True
    n_divided_by_last_num = n / nums[-1]
    if does_nums_add_up_to_n_part2(nums[:-1], n_divided_by_last_num):
        return True
    if n_ends_with_n2(n, nums[-1]):
        if does_nums_add_up_to_n_part2(
            nums[:-1], int(str(int(n)).removesuffix(str(nums[-1])) or "0")
        ):
            return True
    return False


def part1(test_input: bool = False) -> None:
    text = get_input_text(7, test_input=test_input)

    lines = text.splitlines()
    total: int = 0
    for line in lines:
        answer_str, rest = line.split(": ")
        answer = int(answer_str)
        nums = [int(x) for x in rest.split(" ")]
        result = does_nums_add_up_to_n(nums, answer)
        print(f"{answer}: {rest} -> {result}")
        if result is True:
            total += answer

    print(f"Sum of valid totals is {total}")


def part2(test_input: bool = False) -> None:
    text = get_input_text(7, test_input=test_input)
    lines = text.splitlines()
    total: int = 0
    for line in lines:
        answer_str, rest = line.split(": ")
        answer = int(answer_str)
        nums = [int(x) for x in rest.split(" ")]
        result = does_nums_add_up_to_n_part2(nums, answer)
        # print(f"{answer}: {rest} -> {result}")
        if result is True:
            total += answer

    print(f"Sum of valid totals is {total}")


def n_ends_with_n2(n: float, n2: int) -> bool:
    if not assert_float_is_just_int(n, debug=True):
        return False
    n_int = int(n)
    return (
        str(n_int).find(
            str(n2),
            (len(str(n_int)) - len(str(n2))),
        )
        != -1
    )


if __name__ == "__main__":
    part2(test_input=False)
