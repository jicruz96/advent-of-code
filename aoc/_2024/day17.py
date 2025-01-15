from __future__ import annotations

import re
from functools import cached_property
from typing import Any, Callable, Literal, NamedTuple, TypeAlias

from rich import print

from aoc.helpers import get_input_text

INPUT_PATTERN = r"""
Register A: (\d+)
Register B: (\d+)
Register C: (\d+)

Program: (.*)
""".strip()

Register: TypeAlias = Literal["A", "B", "C"]


class InvalidComboOperandError(Exception):
    pass


class InputData(NamedTuple):
    register_a_start_value: int
    register_b_start_value: int
    register_c_start_value: int

    instructions: list[int]
    part2: bool = False

    @classmethod
    def load(cls, test_input: bool = False) -> InputData:
        text = get_input_text(17, test_input=test_input).strip()
        match = re.fullmatch(INPUT_PATTERN, text)
        if match is None:
            raise ValueError(
                f"Input text did not match expected pattern.\nExpected:\n{INPUT_PATTERN}\nGot:\n{text}"
            )
        return cls(
            register_a_start_value=int(match.group(1)),
            register_b_start_value=int(match.group(2)),
            register_c_start_value=int(match.group(3)),
            instructions=list(map(int, match.group(4).split(","))),
        )


class Day17Interpreter:
    registers: dict[Register, int]
    instructions: list[int]
    instruction_pointer: int
    output: list[int]
    part2: bool

    def __init__(self, data: InputData) -> None:
        self.registers = {
            # part 2: what initial value will provoke
            #        the program to print itself?
            "A": data.register_a_start_value,
            "B": data.register_b_start_value,
            "C": data.register_c_start_value,
        }
        self.instructions = data.instructions
        self.instruction_pointer = 0
        self.output = []
        self.part2 = data.part2
        self.halt = False

    def combo(self, operand: int) -> int:
        if operand <= 3:
            return operand
        if operand == 4:
            return self.registers["A"]
        if operand == 5:
            return self.registers["B"]
        if operand == 6:
            return self.registers["C"]
        raise InvalidComboOperandError(str(operand))

    def bxl(self, operand: int) -> None:
        self.registers["B"] ^= operand

    def bst(self, operand: int) -> None:
        self.registers["B"] = self.combo(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.registers["A"] != 0:
            self.instruction_pointer = operand

    def bxc(self, operand: int) -> None:
        self.registers["B"] ^= self.registers["C"]

    def out(self, operand: int) -> None:
        self.output.append(self.combo(operand) % 8)
        # if self.output[-1] != self.instructions[len(self.output) - 1]:
        #     self.halt = True
        # self.status()

    def _dv(self, operand: int, to_register: Register) -> None:
        self.registers[to_register] = self.registers["A"] // (2 ** self.combo(operand))

    def adv(self, operand: int) -> None:
        self._dv(operand, to_register="A")

    def bdv(self, operand: int) -> None:
        self._dv(operand, to_register="B")

    def cdv(self, operand: int) -> None:
        self._dv(operand, to_register="C")

    @cached_property
    def opcodes(self) -> dict[int, Callable[[int], None]]:
        return {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def status(self) -> None:
        def binary_repr(v: Any) -> str:
            return f"{v:048b}"

        # a_binary_repr = f"{self.registers['A']:b}"
        # prev_i = 0
        # chunks: list[str] = []
        # for i in range(3, len(a_binary_repr), 3):
        #     binary_chunk = a_binary_repr[prev_i:i]
        #     prev_i = i
        #     chunks.append(binary_chunk)
        x = self.registers["C"] | 5
        x_bin_rep = binary_repr(x)
        registers: dict[str, tuple[str, int]] = {
            "A    ": (binary_repr(self.registers["A"]), self.registers["A"]),
            "C    ": (binary_repr(self.registers["C"]), self.registers["C"]),
            # "C | 5": (x_bin_rep, x),
            "B    ": (binary_repr(self.registers["B"]), self.registers["B"]),
        }
        print(registers)

    def run(self) -> list[int]:
        # self.status()
        # while not self.halt and self.instruction_pointer < len(self.instructions) - 1:
        while self.instruction_pointer < len(self.instructions) - 1:
            opcode = self.instructions[self.instruction_pointer]
            operand = self.instructions[self.instruction_pointer + 1]
            op = self.opcodes[opcode]
            op(operand)
            # print(
            #     f"[{self.instruction_pointer}] {opcode=} op={op.__name__} {operand=} {self.registers=}"
            # )
            # i.e. update instruction pointer (unless we executed jnz ("jump") command)
            if opcode != 3 or self.registers["A"] == 0:
                self.instruction_pointer = self.instruction_pointer + 2
        return self.output


def part1():
    output = Day17Interpreter(InputData.load()).run()
    print(",".join(map(str, output)))


def part2():
    """
    # I manually converted my puzzle input
    # into the pseudocode below:
    while registerA != 0:
        registerB = (registerA % 8) ^ 0b101 ^ (registerA // (2 ** registerB))
        registerA = registerA // 8
        print(registerB % 8)


    # this means that the solution basically amounts to answering:
    #
    # "what initial number for registerA will provoke the modulus of registerB
    # to correspond to the instruction set?"
    #
    # the exact registerB calculation going isn't relevant... _i think_.

    # i still got stuck on the exact registerB calculation. Namely, I kept trying to
    # find a discernable, predictable pattern in how registerA produced a value into registerC
    # and how that produced a value into registerB.

    # i think we're just supposed to know that registerB % 8 is some function of registerA.


    # also, it means registerA must necessarily be greater than 8^(len(instructions) - 1)
    # to ensure that the while loop runs enough times to print enough output.


    # also, the fact that the operations are basically just glorified bit manipulations,
    # that suggests that we can finesse the right answer by thinking of this problem in
    # terms of bit representations.... i think....
    """
    data = InputData.load(test_input=False)
    a = 0
    for i in reversed(range(len(data.instructions))):
        a <<= 3
        while (
            Day17Interpreter(
                InputData(
                    register_a_start_value=a,
                    register_b_start_value=data.register_b_start_value,
                    register_c_start_value=data.register_c_start_value,
                    instructions=data.instructions,
                )
            ).run()
            != data.instructions[i:]
        ):
            a += 1
    print(f"Minimal register A start value needed {a}")


part2()
