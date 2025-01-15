from __future__ import annotations

import re
from typing import Generator, NamedTuple

from aoc.helpers import get_input_text

WIRE_CONNECTION_PATTERN = re.compile(
    r"(?P<i1>.*?) (?P<op>AND|OR|XOR) (?P<i2>.*?) -> (?P<o>.*?)"
)


def process(op: str, op1: int, op2: int) -> int:
    if op == "AND":
        return op1 & op2
    elif op == "OR":
        return op1 | op2
    elif op == "XOR":
        return op1 ^ op2
    raise ValueError(f"Unknown op {op!r}")


class WireConnection(NamedTuple):
    input_1: str
    input_2: str
    op: str
    output: str

    @property
    def inputs(self) -> tuple[str, str]:
        return (self.input_1, self.input_2)

    @property
    def wires(self) -> tuple[str, str, str]:
        return (*self.inputs, self.output)


class Day24Data(NamedTuple):
    wire_states: dict[str, int]
    output_to_inputs: dict[str, WireConnection]

    def iter_connections(self) -> Generator[WireConnection]:
        yield from self.output_to_inputs.values()

    def iter_outputs(self) -> Generator[str]:
        yield from self.output_to_inputs.keys()

    @property
    def highest_z(self) -> str:
        return max(o for o in self.iter_outputs() if o.startswith("z"))

    @property
    def input_to_outputs(self) -> dict[str, list[WireConnection]]:
        input_to_outputs: dict[str, list[WireConnection]] = {}
        for conn in self.output_to_inputs.values():
            for _input in conn.inputs:
                if _input not in input_to_outputs:
                    input_to_outputs[_input] = []
            input_to_outputs[conn.input_1].append(conn)
            input_to_outputs[conn.input_2].append(conn)
        return input_to_outputs

    @classmethod
    def load(cls, test_input: bool = False) -> Day24Data:
        text = get_input_text(24, test_input=test_input)
        initial_wire_values_section_text, wire_connections_section_text = text.split(
            "\n\n"
        )
        wire_states: dict[str, int] = {}
        for line in initial_wire_values_section_text.splitlines():
            wire, state = line.split(": ")
            wire_states[wire] = int(state)
        wire_connections: dict[str, WireConnection] = {}
        for line in wire_connections_section_text.splitlines():
            match = re.fullmatch(WIRE_CONNECTION_PATTERN, line)
            assert match is not None
            output_wire = match.group("o")
            input_wire_1 = match.group("i1")
            input_wire_2 = match.group("i2")
            op = match.group("op")
            wire_connections[output_wire] = WireConnection(
                input_1=input_wire_1,
                input_2=input_wire_2,
                op=op,
                output=output_wire,
            )
        return cls(wire_states, wire_connections)

    def get_wire_state(self, wire: str) -> int:
        if wire in self.wire_states:
            return self.wire_states[wire]
        if wire not in self.output_to_inputs:
            raise ValueError(f"Unknown wire {wire!r}")
        i1, i2, op, _ = self.output_to_inputs[wire]
        assert op in ("AND", "OR", "XOR")
        i1_state = self.get_wire_state(i1)
        i2_state = self.get_wire_state(i2)
        wire_state = process(op, i1_state, i2_state)
        return wire_state


def part1() -> None:
    data = Day24Data.load(test_input=False)
    z_wire_states: list[str] = [""] * (int(data.highest_z[1:]) + 1)
    for wire in data.iter_outputs():
        if wire.startswith("z"):
            z_wire_states[int(wire[1:])] = str(data.get_wire_state(wire))
    z_number_repr = "".join(reversed(z_wire_states))
    z_number = int(z_number_repr, 2)
    # from rich import print

    # print(
    #     "\n".join(
    #         [
    #             f"{item[0]}: {item[1]}"
    #             for item in sorted(
    #                 data.wire_states.items(),
    #                 key=lambda item: item[0],
    #             )
    #         ]
    #     )
    # )
    print(f"{len(z_number_repr)=} {z_number_repr=} {z_number=}")


def part2() -> None:
    """Credit to Iscddit:
    https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3kt1je
    """
    data = Day24Data.load(test_input=False)

    def is_wrong(conn: WireConnection) -> bool:
        subconnections = data.input_to_outputs.get(conn.output, [])
        return (
            (
                conn.op != "XOR"
                and conn.output.startswith("z")
                and conn.output != data.highest_z
            )
            or (
                conn.op == "XOR"
                and (
                    all(not wire.startswith(("x", "y", "z")) for wire in conn.wires)
                    or any(subconn.op == "OR" for subconn in subconnections)
                )
            )
            or (
                conn.op == "AND"
                and "x00" not in conn.inputs
                and any(subconn.op != "OR" for subconn in subconnections)
            )
        )

    wrong = [conn.output for conn in data.iter_connections() if is_wrong(conn)]
    print(",".join(sorted(wrong)))


if __name__ == "__main__":
    part1()
    part2()
