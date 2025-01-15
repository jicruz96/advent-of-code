from collections import deque

from rich import print

from aoc.helpers import Grid


def find_shortest_path(
    grid: Grid[str],
    start: tuple[int, int],
    end: tuple[int, int],
) -> list[tuple[int, int]] | None:
    queue = deque[tuple[int, int, list[tuple[int, int]]]](
        [(start[0], start[1], [start])]
    )
    seen = set[tuple[int, int]]()
    while queue:
        i, j, path = queue.popleft()
        if i == end[0] and j == end[1]:
            return path
        for neighbor in grid.get_nondiagonal_neighbors((i, j)):
            if neighbor.value in (".", "E") and neighbor.coords not in seen:
                seen.add(neighbor.coords)
                queue.append((neighbor.i, neighbor.j, path + [neighbor.coords]))
    return None
    # raise ValueError(f"Cannot get from {start} to {end}")


def part1(test_input: bool = False) -> None:
    grid = Grid.for_day(20, test_input=test_input)
    start = grid.first("S", strict=True)
    end = grid.first("E", strict=True)
    path = find_shortest_path(grid, start.coords, end.coords)
    if path is None:
        raise ValueError
    # print(
    #     "\n".join(
    #         [
    #             "".join(
    #                 [
    #                     grid[i][j] if (i, j) not in path else "O"
    #                     for j in range(len(grid[i]))
    #                 ]
    #             )
    #             for i in range(len(grid))
    #         ]
    #     )
    # )
    all_cheats_by_distance: dict[
        int, list[tuple[tuple[int, int], tuple[int, int]]]
    ] = {}
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            spot1 = path[i]
            spot2 = path[j]
            if (
                spot1[0] == spot2[0]
                and abs(spot1[1] - spot2[1]) == 2
                and grid.at((spot1[0], max(spot1[1], spot2[1]) - 1), strict=True).value
                == "#"
            ) or (
                spot1[1] == spot2[1]
                and abs(spot1[0] - spot2[0]) == 2
                and grid.at((max(spot1[0], spot2[0]) - 1, spot1[1]), strict=True).value
                == "#"
            ):
                cheat_distance = abs(i - j) - 2
                assert cheat_distance >= 0
                if cheat_distance not in all_cheats_by_distance:
                    all_cheats_by_distance[cheat_distance] = []
                all_cheats_by_distance[cheat_distance].append((spot1, spot2))
    cheats_over_99 = 0
    for dist, cheats in all_cheats_by_distance.items():
        if dist > 99:
            cheats_over_99 += len(cheats)
    print(f"{cheats_over_99=}")


def part2(test_input: bool = False) -> None:
    grid = Grid.for_day(20, test_input=test_input)
    start = grid.first("S", strict=True)
    end = grid.first("E", strict=True)
    path = find_shortest_path(grid, start.coords, end.coords)
    if path is None:
        raise ValueError
    # print(
    #     "\n".join(
    #         [
    #             "".join(
    #                 [
    #                     grid[i][j] if (i, j) not in path else "O"
    #                     for j in range(len(grid[i]))
    #                 ]
    #             )
    #             for i in range(len(grid))
    #         ]
    #     )
    # )
    cheats_by_distance: dict[int, int] = {}
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            spot1 = path[i]
            spot2 = path[j]
            delta_x = abs(spot1[0] - spot2[0])
            delta_y = abs(spot1[1] - spot2[1])
            total_absolute_distance = delta_x + delta_y
            cheat_distance = abs(i - j) - total_absolute_distance
            if cheat_distance <= 0 or total_absolute_distance > 20:
                continue
            if cheat_distance not in cheats_by_distance:
                cheats_by_distance[cheat_distance] = 0
            cheats_by_distance[cheat_distance] += 1
    cheats_over_99 = 0
    if test_input:
        items = sorted(
            cheats_by_distance.items(),
            key=lambda item: item[0],
        )
    else:
        items = cheats_by_distance.items()
    for dist, cheats in items:
        if dist > 99:
            cheats_over_99 += cheats
        if test_input and dist >= 50:
            print(f"- There are {cheats} cheats that save {dist} picoseconds.")
    print(f"{cheats_over_99=}")


part2(test_input=False)
