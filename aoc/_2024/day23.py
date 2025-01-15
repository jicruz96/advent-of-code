from __future__ import annotations

import functools
import itertools
from typing import Callable

from aoc.helpers import get_input_text


def sorted_tuple(*items: str) -> tuple[str, ...]:
    return tuple(sorted(items))


class Graph(dict[str, list[str]]):
    def __init__(self):
        super().__init__()

        @functools.cache
        def complete_sets_of_size_n_that_contain_node(
            node: str, n: int
        ) -> set[tuple[str, ...]]:
            if n < 2:
                raise ValueError
            if n == 2:
                return {sorted_tuple(node, neighbor) for neighbor in self[node]}
            sets: set[tuple[str, ...]] = set()
            for neighbor in self.get(node, []):
                neighbor_sets = self.complete_sets_of_size_n_that_contain_node(
                    neighbor, n - 1
                )
                for neighbor_set in neighbor_sets:
                    if node not in neighbor_set and all(
                        node in self[set_member] for set_member in neighbor_set
                    ):
                        sets.add(sorted_tuple(*neighbor_set, node))
            return sets

        self.complete_sets_of_size_n_that_contain_node = (
            complete_sets_of_size_n_that_contain_node
        )

    def get_complete_sets_of_size_n_in_graph(
        self,
        n: int,
        filter: Callable[[str], bool] | None = None,
    ) -> set[tuple[str, ...]]:
        unique_complete_sets = set[tuple[str, ...]]()
        for node in self:
            if filter is None or filter(node):
                unique_complete_sets.update(
                    self.complete_sets_of_size_n_that_contain_node(node, n)
                )
        return unique_complete_sets

    @classmethod
    def for_day_23(cls, test_input: bool = False) -> Graph:
        text = get_input_text(23, test_input=test_input)
        nodes: dict[str, list[str]] = cls()
        for line in text.splitlines():
            comp1, comp2 = line.split("-")
            if comp1 not in nodes:
                nodes[comp1] = []
            if comp2 not in nodes:
                nodes[comp2] = []
            nodes[comp1].append(comp2)
            nodes[comp2].append(comp1)
        return nodes


def part1(graph: Graph):
    print(
        len(
            graph.get_complete_sets_of_size_n_in_graph(
                n=3,
                filter=lambda node: node[0] == "t",
            )
        )
    )


def part2(graph: Graph):
    prev_unique_complete_sets = set[tuple[str, ...]]()
    for n in itertools.count(start=3):
        unique_comple_sets = graph.get_complete_sets_of_size_n_in_graph(n)
        if not unique_comple_sets:
            break
        prev_unique_complete_sets = unique_comple_sets
        print(n, len(unique_comple_sets))
    assert len(prev_unique_complete_sets) == 1
    print(",".join(list(prev_unique_complete_sets)[0]))


if __name__ == "__main__":
    graph = Graph.for_day_23(test_input=False)
    part1(graph)
    part2(graph)
