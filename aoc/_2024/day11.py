"""https://adventofcode.com/2024/day/11"""

from __future__ import annotations

from rich import print

from aoc.helpers import get_input_text

DAY_NUM = 11


class Stone:
    def __init__(self, n: int):
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self) -> str:
        return str(self)

    def blink(self) -> list[Stone]:
        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        if self.n == 0:
            return [Stone(1)]

        # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        n_str = str(self.n)
        if len(n_str) % 2 == 0:
            return [
                Stone(int(n_str[: len(n_str) // 2])),
                Stone(int(n_str[len(n_str) // 2 :])),
            ]

        # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
        return [
            Stone(self.n * 2024),
        ]


def part1(test_input: bool = False) -> None:
    text = get_input_text(DAY_NUM, test_input=test_input).strip()
    stones = [Stone(int(num_str)) for num_str in text.split()]
    for _ in range(25):
        if _ <= 6 and test_input:
            print(_, stones)
        new_stones: list[Stone] = []
        for stone in stones:
            result_stones = stone.blink()
            new_stones.extend(result_stones)
        stones = new_stones
        print(f"There are {len(stones)} stones after {_ + 1} iterations.")


def part2(test_input: bool = False) -> None:
    cache: dict[tuple[int, int], int] = {}
    MAX_ITERATION = 75

    def get_stone_count_for_n(n: int, iterations_left: int = MAX_ITERATION) -> int:
        assert iterations_left >= 0 and iterations_left <= MAX_ITERATION
        if cache.get((n, iterations_left)) is None:
            if iterations_left == 0:
                result = 1
            elif n == 0:
                result = get_stone_count_for_n(1, iterations_left - 1)
            elif len(str(n)) % 2 == 0:
                n_str = str(n)
                left_n = int(n_str[: len(n_str) // 2])
                right_n = int(n_str[len(n_str) // 2 :])
                stones_produced_by_left_child = get_stone_count_for_n(
                    left_n, iterations_left - 1
                )
                stones_produced_by_right_child = get_stone_count_for_n(
                    right_n, iterations_left - 1
                )
                result = stones_produced_by_left_child + stones_produced_by_right_child
            else:
                result = get_stone_count_for_n(n * 2024, iterations_left - 1)
            cache[(n, iterations_left)] = result
        return cache[(n, iterations_left)]

    text = get_input_text(DAY_NUM, test_input=test_input).strip()
    stone_nums = list(map(int, text.split()))
    total: int = 0
    for stone_num in stone_nums:
        result = get_stone_count_for_n(n=stone_num)
        total += result
    print(f"There are {total} stones after {MAX_ITERATION} iterations")


if __name__ == "__main__":
    # part1(test_input=True)
    part2(test_input=False)
