"""https://adventofcode.com/2024/day/15"""

from typing import Literal

# from rich import print
from aoc.helpers import Cell, Grid, get_input_text

Direction = Literal[">", "<", "v", "^"]


# first let's make the "map"
class LanternfishWarehouseRobotMap:
    def __init__(self, test_input: bool = False, debug: bool = False):
        text = get_input_text(15, test_input=test_input)
        warehouse_map_text, robot_directions = text.split("\n\n")
        self.test_input = test_input
        self.debug = debug
        self.warehouse_map_text = warehouse_map_text.strip()
        self.robot_directions = list(robot_directions.strip().replace("\n", ""))

    def solve_part_1(self):
        warehouse_map = Grid(
            [list(line) for line in self.warehouse_map_text.splitlines()]
        )
        robot = warehouse_map.first("@")
        if robot is None:
            raise ValueError(f"Could not find robot in {warehouse_map}")
        # print(warehouse_map)
        for direction_i in range(len(self.robot_directions)):
            # what do we do here?
            direction = self.robot_directions[direction_i]
            # print(f"{direction=}.")
            assert direction in (">", "<", "v", "^")

            # we go to the robot position.

            # we say, hey, what's in the position you're trying to move to?
            delta_i = (direction == "v") - (direction == "^")
            delta_j = (direction == ">") - (direction == "<")
            next_i, next_j = (robot.i + delta_i, robot.j + delta_j)
            boxes_next_to_robot = False
            while (
                cell := warehouse_map.at((next_i, next_j), strict=True)
            ).value == "O":
                next_i += delta_i
                next_j += delta_j
                boxes_next_to_robot = True
            if cell.value != "#":
                assert cell.value == ".", ValueError(cell.value)
                warehouse_map[robot.i][robot.j] = "."
                robot = warehouse_map.at(
                    (robot.i + delta_i, robot.j + delta_j), strict=True
                )
                warehouse_map[robot.i][robot.j] = "@"
                if boxes_next_to_robot:
                    warehouse_map[cell.i][cell.j] = "O"
            # print grid to make sure everything looks right
            # print(
            #     f"Move {direction}:\n{warehouse_map}\nNext move: {self.robot_directions[direction_i + 1] if direction_i < len(self.robot_directions) - 1 else "None"}"
            # )
            # breakpoint()
        # print("")
        # after all moves, calculate sum of boxes's GPS value
        gps_sum = 0
        for cell in warehouse_map.traverse():
            if cell.value == "O":
                gps_value = 100 * cell.i + cell.j
                # print(
                #     f"Box({cell.i}, {cell.j}) GPS: 100 * {cell.i} + {cell.j} = {gps_value}"
                # )
                gps_sum += gps_value

        print(f"sum of all boxes' GPS coordinates after robot moves: {gps_sum}")

    def solve_part_2(self):
        widened_warehouse_map_text = ""
        for line in self.warehouse_map_text.splitlines():
            for char in line:
                if char == "#":
                    widened_warehouse_map_text += "##"
                elif char == "O":
                    widened_warehouse_map_text += "[]"
                elif char == ".":
                    widened_warehouse_map_text += ".."
                elif char == "@":
                    widened_warehouse_map_text += "@."
                else:
                    raise ValueError(f"Unknown character in input text: {char!r}")
            widened_warehouse_map_text += "\n"
        # [[char for char in line] for line in self.warehouse_map_text.splitlines()]
        warehouse_map = Grid(
            [list(line) for line in widened_warehouse_map_text.splitlines()]
        )

        def get_cell_box_pair(cell: Cell) -> tuple[Cell, Cell]:
            if cell.value == "[":
                partner = warehouse_map.at((cell.i, cell.j + 1), strict=True)
                expected = "]"
                first, second = cell, partner
            elif cell.value == "]":
                partner = warehouse_map.at((cell.i, cell.j - 1), strict=True)
                expected = "["
                first, second = partner, cell
            else:
                raise ValueError(
                    f"Cell({cell.i}, {cell.j})[{cell.value!r}] is not a box cell."
                )
            if partner.value != expected:
                ValueError(
                    f"Cell({cell.i}, {cell.j}): expected partner Cell({partner.i}, {partner.j}) "
                    f"to have value '{expected}' but has value {partner.value}"
                )
            return first, second

        robot = warehouse_map.first("@")
        if robot is None:
            raise ValueError(f"Could not find robot in {warehouse_map}")
        if self.debug:
            print(warehouse_map)
        for direction_i in range(len(self.robot_directions)):
            direction = self.robot_directions[direction_i]
            assert direction in (">", "<", "v", "^")
            delta_i = (direction == "v") - (direction == "^")
            delta_j = (direction == ">") - (direction == "<")
            boxes_next_to_robot: list[tuple[Cell, Cell]] = []
            box_cell_positions: set[tuple[int, int]] = set()
            next_spot = warehouse_map.at((robot.i + delta_i, robot.j + delta_j))
            if next_spot is None:
                breakpoint()
                raise ValueError
            elif next_spot.value == "#":
                if self.debug:
                    print("Cannot move!")
            else:
                neighbors_to_check: list[Cell] = [next_spot]

                # * ok, up til here all the logic is the same...
                def eval_cell_boxiness(cell: Cell) -> None:
                    def queue_up_neighbors_if_needed(cell: Cell):
                        neighbor_i = cell.i + delta_i
                        neighbor_j = cell.j + delta_j
                        neighbor = warehouse_map.at(
                            (neighbor_i, neighbor_j), strict=True
                        )
                        if neighbor.coords not in box_cell_positions:
                            neighbors_to_check.append(neighbor)

                    if cell.value in "[]" and cell.coords not in box_cell_positions:
                        box_pair = get_cell_box_pair(cell)
                        boxes_next_to_robot.append(box_pair)
                        box_cell_positions.add(box_pair[0].coords)
                        box_cell_positions.add(box_pair[1].coords)
                        # get coordinates to check for boxiness that are influenced by
                        # box pair
                        queue_up_neighbors_if_needed(box_pair[0])
                        queue_up_neighbors_if_needed(box_pair[1])

                while neighbors_to_check:
                    neighbor = neighbors_to_check.pop(0)
                    eval_cell_boxiness(neighbor)

                # at this point we should have all boxes in the boxes_next_to_robot.
                if self.debug:
                    print(f"{boxes_next_to_robot=}")

                # if any of the boxes are not movable, then we're not movable. continue
                def box_is_movable(box: tuple[Cell, Cell]) -> bool:
                    if direction == "<":
                        neighbor = warehouse_map.at(
                            (box[0].i, box[0].j - 1), strict=True
                        )
                        return neighbor.value != "#"
                    elif direction == ">":
                        neighbor = warehouse_map.at(
                            (box[1].i, box[1].j + 1), strict=True
                        )
                        return neighbor.value != "#"
                    elif direction == "^":

                        def foobar(cell: Cell) -> bool:
                            neighbor = warehouse_map.at(
                                (cell.i - 1, cell.j), strict=True
                            )
                            return neighbor.value != "#"

                        return foobar(box[0]) and foobar(box[1])
                    elif direction == "v":

                        def foobar(cell: Cell) -> bool:
                            neighbor = warehouse_map.at(
                                (cell.i + 1, cell.j), strict=True
                            )
                            return neighbor.value != "#"

                        return foobar(box[0]) and foobar(box[1])
                    else:
                        raise ValueError(f"What direction is this {direction!r}")

                if not all(box_is_movable(box) for box in boxes_next_to_robot):
                    if self.debug:
                        print("Cannot move!")
                else:
                    # okay now we move the boxes.
                    for box in boxes_next_to_robot:
                        left_side, right_side = box
                        warehouse_map[left_side.i][left_side.j] = "."
                        warehouse_map[right_side.i][right_side.j] = "."
                    for box in boxes_next_to_robot:
                        left_side, right_side = box
                        warehouse_map[left_side.i + delta_i][left_side.j + delta_j] = (
                            "["
                        )
                        warehouse_map[right_side.i + delta_i][
                            right_side.j + delta_j
                        ] = "]"

                    # and lastly we move the robot
                    warehouse_map[robot.i][robot.j] = "."
                    warehouse_map[robot.i + delta_i][robot.j + delta_j] = "@"
                    robot = warehouse_map.at(
                        (robot.i + delta_i, robot.j + delta_j), strict=True
                    )

            # print grid to make sure everything looks right
            if self.debug:
                print(
                    f"Move {direction}:\n{warehouse_map}\nNext move: {self.robot_directions[direction_i + 1] if direction_i < len(self.robot_directions) - 1 else 'None'}"
                )
                # breakpoint()
        # after all moves, calculate sum of boxes's GPS value
        gps_sum = 0
        for cell in warehouse_map.traverse():
            if cell.value == "[":
                gps_value = 100 * cell.i + cell.j
                # print(
                #     f"Box({cell.i}, {cell.j}) GPS: 100 * {cell.i} + {cell.j} = {gps_value}"
                # )
                gps_sum += gps_value

        print(f"sum of all boxes' GPS coordinates after robot moves: {gps_sum}")


print("------------------------------" * 4)
LanternfishWarehouseRobotMap().solve_part_2()
