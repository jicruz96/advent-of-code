"""https://adventofcode.com/2024/day/5"""

from __future__ import annotations

from typing import Literal, overload

from rich import print

from aoc.helpers import get_input_text


def part1(test_input: bool = False) -> None:
    text = get_input_text(5, test_input=test_input)
    ordering_text, updates_text = text.split("\n\n")
    ordering_lines = ordering_text.splitlines()
    joe: dict[int, list[int]] = {}
    for line in ordering_lines:
        # each line should be of the form X|Y
        x_str, y_str = line.split("|")
        x = int(x_str)
        y = int(y_str)
        if x not in joe:
            joe[x] = []
        joe[x].append(y)
    updates_lines = updates_text.splitlines()
    valid_lines: list[str] = []
    for update_line in updates_lines:
        is_valid: bool = True
        nums = list(map(int, update_line.split(",")))
        for n in nums:
            things_that_should_go_after_n = joe.get(n, [])
            for y in things_that_should_go_after_n:
                if y in nums and nums.index(y) <= nums.index(n):
                    is_valid = False
                    break
        if is_valid:
            valid_lines.append(update_line)

    # return total sum of middle numbers of valid "update" lines.
    total: int = 0
    for update_line in valid_lines:
        nums = list(map(int, update_line.split(",")))
        total += nums[len(nums) // 2]

    print("Sum of middle numbers of valid lines is", total)


# restarting part 2. no peeking at part 1 either.
def part2(test_input: bool = False) -> None:
    text = get_input_text(5, test_input=test_input)
    ordering_section, updates_section = text.split("\n\n")

    class Node:
        n: int
        children: list[Node]

        def __init__(self, n: int):
            self.n = n
            self.children = []

        def get_child(self, n: int) -> Node | None:
            for child in self.children:
                if child.n == n:
                    return child
            return None

    class Graph:
        nodes: dict[int, Node]

        def __init__(self):
            self.nodes = {}

        @overload
        def get(
            self, n: int, create_if_not_exists: Literal[False] = False
        ) -> Node | None:
            pass

        @overload
        def get(self, n: int, create_if_not_exists: Literal[True]) -> Node:
            pass

        def get(self, n: int, create_if_not_exists: bool = False) -> Node | None:
            for node in self.nodes.values():
                if node.n == n:
                    return node
            if create_if_not_exists:
                node = Node(n)
                self.nodes[n] = node
                return node
            return None

        def is_traversable_sequence(self, seq: list[int]) -> bool:
            seq = seq.copy()
            if not seq:
                return True
            n = seq.pop(0)
            prev = self.get(n)
            if not prev:
                return False
            while seq:
                n = seq.pop(0)
                node = prev.get_child(n)
                if not node:
                    return False
                prev = node
            return True

    graph = Graph()
    for line in ordering_section.splitlines():
        x_str, y_str = line.split("|")
        x_node = graph.get(int(x_str), create_if_not_exists=True)
        y_node = graph.get(int(y_str), create_if_not_exists=True)
        x_node.children.append(y_node)

    total = 0
    for line in updates_section.splitlines():
        nums = list(map(int, line.split(",")))
        if graph.is_traversable_sequence(nums):
            continue
        fixed_nums: list[int] = []
        for num in nums:
            inserted: bool = False
            for i in range(len(fixed_nums)):
                node = graph.get(fixed_nums[i])
                assert node is not None
                if not node.get_child(num):
                    fixed_nums.insert(i, num)
                    inserted = True
                    break
            if not inserted:
                fixed_nums.append(num)
        assert len(nums) == len(fixed_nums)
        assert graph.is_traversable_sequence(fixed_nums)
        total += fixed_nums[len(fixed_nums) // 2]
    print(
        "The sum of the middle number of all fixed, originally invalid sequences is",
        total,
    )


if __name__ == "__main__":
    part2(test_input=False)
