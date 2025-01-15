from collections import deque
from typing import Literal, NamedTuple, TypeAlias

from rich import print

from aoc.helpers import Cell, Grid

Orientation: TypeAlias = Literal["east", "west", "north", "south"]
ScoreAndOrientationsThatGotUsToThisCell: TypeAlias = list[tuple[int, Orientation]]


class PositionData(NamedTuple):
    cell: Cell[str]
    orientation: Orientation


def get_pivot_score(current: Orientation, target: Orientation) -> int:
    if current == target:
        return 0
    if current in ("east", "west"):
        return 1_000 if target in ("north", "south") else 2_000
    return 1_000 if target in ("east", "west") else 2_000


def solve(maze: Grid[str], *, part2: bool = False) -> None:
    print(maze)

    # find start and end positions
    start = maze.first("S", strict=True)

    # keep a copy of the maze where you keep a running tally
    # of the minimum score at any given position.
    scores = Grid[dict[Orientation, int | None]].full_of(
        fill=lambda: {
            "east": None,
            "north": None,
            "south": None,
            "west": None,
        },
        size=len(maze),
    )
    scores[start.i][start.j]["east"] = 0

    # now, start at start and move.
    # once all paths have been exhausted, just return
    # the value at the end position.

    queue = deque[PositionData]([PositionData(cell=start, orientation="east")])

    # try to move up
    def move_and_update_score(
        current_position_data: PositionData,
        destination_coords: tuple[int, int],
        required_orientation: Orientation,
    ) -> None:
        destination = maze.at(destination_coords)
        if destination is not None and destination.value in (".", "E"):
            current_position_score = scores.at(
                current_position_data.cell.coords, strict=True
            ).value[current_position_data.orientation]
            assert current_position_score is not None
            move_score = (
                1
                + current_position_score
                + get_pivot_score(
                    current_position_data.orientation, required_orientation
                )
            )
            current_destination_score = scores.at(
                destination.coords, strict=True
            ).value[required_orientation]
            if (
                current_destination_score is None
                or move_score < current_destination_score
            ):
                scores[destination.i][destination.j][required_orientation] = move_score
                queue.append(
                    PositionData(cell=destination, orientation=required_orientation)
                )

    while queue:
        pos = queue.popleft()
        move_and_update_score(
            pos,
            (pos.cell.i - 1, pos.cell.j),
            required_orientation="north",
        )
        move_and_update_score(
            pos,
            (pos.cell.i + 1, pos.cell.j),
            required_orientation="south",
        )
        move_and_update_score(
            pos,
            (pos.cell.i, pos.cell.j + 1),
            required_orientation="east",
        )
        move_and_update_score(
            pos,
            (pos.cell.i, pos.cell.j - 1),
            required_orientation="west",
        )
    # max_len = 0
    # for cell in scores.traverse():
    #     min_value = min([val for val in cell.value.values() if val is not None])
    #     max_len = max(max_len, len(str(min_value)))
    # scores_repr = [
    #     [f"{min(scores_dict.values()):{max_len}d}" for scores_dict in row]
    #     for row in scores
    # ]
    # print(scores_repr)
    end = maze.first("E", strict=True)
    end_score_cell = scores.at(end.coords, strict=True)
    end_score_dict = end_score_cell.value
    end_score = min([v for v in end_score_dict.values() if v is not None])
    print(f"Minimal score to reach end is {end_score}")

    if not part2:
        return
    cells_part_of_ideal_paths: set[tuple[int, int]] = {end_score_cell.coords}
    part2_queue = deque[
        tuple[
            Cell[dict[Orientation, int | None]],
            Cell[dict[Orientation, int | None]] | None,
        ]
    ]([(end_score_cell, None)])
    while part2_queue:
        cell, came_from_cell = part2_queue.popleft()
        actual_scores: dict[Orientation, int] = {
            k: v for k, v in cell.value.items() if v is not None
        }
        min_score_orientation = min(
            actual_scores.keys(), key=lambda k: actual_scores[k]
        )
        min_score = actual_scores[min_score_orientation]
        for neighbor in scores.get_nondiagonal_neighbors(cell.coords):
            if neighbor == came_from_cell:
                continue
            if maze.at(neighbor.coords, strict=True).value not in ("S", "E", "."):
                continue

            def foobar(neighbor_orientation: Orientation):
                # neighbor is to cell's east, so we must've been moving west
                if min_score_orientation == neighbor_orientation:
                    assert actual_scores[neighbor_orientation] == min_score
                    assert {
                        "south": (cell.i - 1, cell.j),
                        "north": (cell.i + 1, cell.j),
                        "east": (cell.i, cell.j - 1),
                        "west": (cell.i, cell.j + 1),
                    }[neighbor_orientation] == neighbor.coords
                    cells_part_of_ideal_paths.add(neighbor.coords)
                    part2_queue.append((neighbor, cell))
                    return
                else:
                    # maybe the neighbor is the special case
                    if came_from_cell is None:
                        return
                    if came_from_cell.coords == neighbor.coords:
                        return
                    if (
                        neighbor_orientation not in actual_scores
                        or actual_scores[neighbor_orientation] != min_score + 1_000
                    ):
                        return
                    came_from_actual_scores = {
                        k: v for k, v in came_from_cell.value.items() if v is not None
                    }
                    came_from_min_score_orientation = min(
                        came_from_actual_scores,
                        key=lambda k: came_from_actual_scores[k],
                    )
                    if came_from_min_score_orientation == neighbor_orientation:
                        assert (
                            came_from_actual_scores[neighbor_orientation]
                            == min_score + 1_001
                        )
                        assert actual_scores[neighbor_orientation] == min_score + 1_000
                        assert {
                            "south": (came_from_cell.i - 1, came_from_cell.j),
                            "north": (came_from_cell.i + 1, came_from_cell.j),
                            "east": (came_from_cell.i, came_from_cell.j - 1),
                            "west": (came_from_cell.i, came_from_cell.j + 1),
                        }[neighbor_orientation] == cell.coords
                        cells_part_of_ideal_paths.add(neighbor.coords)
                        part2_queue.append((neighbor, cell))
                        return

            if neighbor.i == cell.i:
                if neighbor.j == cell.j + 1:
                    neighbor_orientation = "west"
                else:
                    assert neighbor.j == cell.j - 1
                    neighbor_orientation = "east"
            else:
                assert neighbor.j == cell.j
                if neighbor.i == cell.i + 1:
                    neighbor_orientation = "north"
                else:
                    assert neighbor.i == cell.i - 1
                    neighbor_orientation = "south"
            foobar(neighbor_orientation)

    part2_maze_repr = Grid(
        [
            [
                0 if (i, j) in cells_part_of_ideal_paths else maze[i][j]
                for j in range(len(maze[i]))
            ]
            for i in range(len(maze))
        ]
    )
    print(part2_maze_repr)
    print(f"Number of cells part of ideal paths {len(cells_part_of_ideal_paths)}")


def part1(maze: Grid[str]) -> None:
    solve(maze)


def part2(maze: Grid[str]) -> None:
    solve(maze, part2=True)


if __name__ == "__main__":
    test_maze = Grid.for_day(16, test_input=True)
    maze = Grid.for_day(16, test_input=False)
    # part1(maze)
    part2(maze)
