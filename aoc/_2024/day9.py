"""https://adventofcode.com/2024/day/9"""

from __future__ import annotations

from aoc.helpers import get_input_text

DAY_NUM = 9


def part1(test_input: bool = False) -> None:
    text = get_input_text(DAY_NUM, test_input=test_input)
    text = text.strip()
    # convert text string to representation of disk space
    disk_map: list[str] = []
    file_id: int = 0
    for i in range(len(text)):
        is_file_size_repr = i % 2 == 0
        char = text[i]
        if is_file_size_repr:
            for _ in range(int(char)):
                disk_map.append(str(file_id))
            file_id += 1
        else:
            for _ in range(int(char)):
                disk_map.append(".")
    # now update disk map by "moving" over leftmost
    # file blocks into free space
    free_space_i: int = 0
    file_block_i: int = len(disk_map) - 1
    if test_input:
        print("|".join(disk_map))
    while (
        free_space_i < file_block_i
        and free_space_i < len(disk_map)
        and file_block_i >= 0
    ):
        while free_space_i < file_block_i and free_space_i < len(disk_map):
            if disk_map[free_space_i] == ".":
                break
            free_space_i += 1

        while file_block_i >= 0 and file_block_i > free_space_i:
            if disk_map[file_block_i] != ".":
                break
            file_block_i -= 1

        if (
            file_block_i < 0
            or free_space_i >= file_block_i
            or free_space_i >= len(disk_map)
        ):
            break

        assert disk_map[file_block_i] != "."
        assert disk_map[free_space_i] == "."

        disk_map[free_space_i] = disk_map[file_block_i]
        disk_map[file_block_i] = "."
        free_space_i += 1
        file_block_i -= 1
        # if test_input:
        #     print("".join(disk_map))

    # compute checksum
    checksum: int = 0
    for i in range(len(disk_map)):
        if disk_map[i] != ".":
            checksum += int(disk_map[i]) * i

    print(f"Disk map cheksum: {checksum}")


class Node:
    def __init__(
        self,
        size: int,
        file_id: int | None = None,
        prev: Node | None = None,
        next: Node | None = None,
    ):
        self.size = size
        self.prev = prev
        self.next = next
        self.file_id = file_id

    def as_disk_map(self) -> list[int | None]:
        assert self.prev is None
        disk_map: list[int | None] = []
        node = self
        while node:
            for _ in range(node.size):
                disk_map.append(node.file_id)
            node = node.next
        return disk_map

    def print_disk_map(self) -> None:
        disk_map = self.as_disk_map()
        disk_map_str = [str(x) if x is not None else "." for x in disk_map]
        print("|".join(disk_map_str))


def part2(test_input: bool = False) -> None:
    text = get_input_text(DAY_NUM, test_input=test_input)
    text = text.strip()

    index = 0
    head: Node = Node(
        size=int(text[0]),
        file_id=0,
    )
    file_id: int = 1
    prev: Node = head
    leftmost_space_by_size_cache: list[tuple[Node, int] | None] = [None] * 9
    leftmost_free_space: Node | None = None
    leftmost_free_space_index: int | None = None
    for i in range(1, len(text)):
        is_file_size_repr = i % 2 == 0
        size = int(text[i])
        if is_file_size_repr:
            node = Node(
                size=size,
                file_id=file_id,
                prev=prev,
            )
            index += 1
            file_id += 1
            prev.next = node
            prev = node
            continue
        if size == 0:
            continue
        node = Node(
            size=size,
            file_id=None,
            prev=prev,
        )
        index += 1
        if leftmost_free_space_index is None:
            leftmost_free_space = node
            leftmost_free_space_index = index
        if leftmost_space_by_size_cache[size - 1] is None:
            leftmost_space_by_size_cache[size - 1] = (node, index)
        prev.next = node
        prev = node
    rightmost_space = prev
    rightmost_space_index = index
    assert leftmost_free_space_index is not None
    assert leftmost_free_space is not None
    seen = set[int]()
    # with tqdm(total=file_id) as pbar:
    if test_input:
        print("ORIGINAL")
        head.print_disk_map()
        print("---")
    while rightmost_space and rightmost_space_index > leftmost_free_space_index:
        if rightmost_space.file_id is None:
            rightmost_space = rightmost_space.prev
            rightmost_space_index -= 1
            continue
        assert rightmost_space.file_id is not None
        if rightmost_space.file_id not in seen:
            seen.add(rightmost_space.file_id)
            # pbar.update()
            space: Node | None = None
            space_index: int | None = None
            for i in range(rightmost_space.size - 1, len(leftmost_space_by_size_cache)):
                cache_entry = leftmost_space_by_size_cache[i]
                if (
                    cache_entry is not None
                    and cache_entry[1] < rightmost_space_index
                    and (space_index is None or cache_entry[1] < space_index)
                ):
                    space, space_index = cache_entry
            if space is not None:
                assert space_index is not None
                space.file_id = rightmost_space.file_id
                remaining_size = space.size - rightmost_space.size
                if remaining_size > 0:
                    new_space_node = Node(
                        size=remaining_size,
                        prev=space,
                        next=space.next,
                    )
                    new_space_node_index = space_index + 1
                    rightmost_space_index += 1
                    if space.next:
                        space.next.prev = new_space_node
                    space.next = new_space_node
                    assert remaining_size < 10
                    for i in range(len(leftmost_space_by_size_cache)):
                        cached_node_data = leftmost_space_by_size_cache[i]
                        if (
                            cached_node_data
                            and cached_node_data[1] >= new_space_node_index
                        ):
                            leftmost_space_by_size_cache[i] = (
                                cached_node_data[0],
                                cached_node_data[1] + 1,
                            )
                    john_tuple = leftmost_space_by_size_cache[remaining_size - 1]
                    if john_tuple is None:
                        leftmost_space_by_size_cache[remaining_size - 1] = (
                            new_space_node,
                            new_space_node_index,
                        )
                    else:
                        _, john_index = john_tuple
                        if john_index > new_space_node_index:
                            leftmost_space_by_size_cache[remaining_size - 1] = (
                                new_space_node,
                                new_space_node_index,
                            )
                current_cache_entry = leftmost_space_by_size_cache[space.size - 1]
                if current_cache_entry is not None and current_cache_entry[0] is space:
                    leftmost_space_by_size_cache[space.size - 1] = None
                    jeff = space.next
                    jeff_index = space_index + 1
                    while jeff:
                        if jeff.file_id is None and jeff.size == space.size:
                            leftmost_space_by_size_cache[space.size - 1] = (
                                jeff,
                                jeff_index,
                            )
                            break
                        jeff = jeff.next
                        jeff_index += 1
                space.size = rightmost_space.size
                rightmost_space.file_id = None
                if leftmost_free_space and space is leftmost_free_space:
                    leftmost_free_space = leftmost_free_space.next
                    leftmost_free_space_index += 1
                    while leftmost_free_space:
                        if leftmost_free_space.file_id is None:
                            break
                        leftmost_free_space = leftmost_free_space.next
                        leftmost_free_space_index += 1
                if test_input:
                    head.print_disk_map()
            else:
                rightmost_space = rightmost_space.prev
                rightmost_space_index -= 1
        else:
            rightmost_space = rightmost_space.prev
            rightmost_space_index -= 1

    # compute checksum
    checksum: int = 0
    disk_map = head.as_disk_map()
    if test_input:
        head.print_disk_map()
    for i in range(len(disk_map)):
        val = disk_map[i]
        if val is not None:
            checksum += val * i
    if test_input:
        print()

    print(f"Disk map checksum is {checksum}")


if __name__ == "__main__":
    part1(test_input=False)
    part2(test_input=False)
