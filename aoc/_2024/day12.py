"""https://adventofcode.com/2024/day/12"""

from __future__ import annotations

from rich import print

from aoc.helpers import Cell, Grid


def get_perimeter_at_cell_i_j[T](grid: Grid[T], i: int, j: int) -> int:
    neighbor_values = [cell.value for cell in grid.get_nondiagonal_neighbors((i, j))]
    return 4 - neighbor_values.count(grid[i][j])


def part1(grid: Grid[str]) -> None:
    seen: list[list[bool]] = [[False] * len(grid) for _ in range(len(grid))]

    def find_region_perimeter_and_area(
        cell: Cell[str], region_name: str
    ) -> tuple[int, int]:
        if grid[cell.i][cell.j] != region_name:
            return 0, 0
        perimeter = get_perimeter_at_cell_i_j(grid, cell.i, cell.j)
        area = 1
        seen[cell.i][cell.j] = True
        for diag in grid.get_nondiagonal_neighbors((cell.i, cell.j)):
            if diag.value == region_name and not seen[diag.i][diag.j]:
                cell_area, cell_perimeter = find_region_perimeter_and_area(
                    cell, region_name
                )
                area += cell_area
                perimeter += cell_perimeter
        return area, perimeter

    total_price: int = 0
    for cell in grid.traverse():
        if not seen[cell.i][cell.j]:
            area, perimeter = find_region_perimeter_and_area(cell, cell.value)
            price = area * perimeter
            print(f"{cell.value!r}: {area} * {perimeter} = {price}")
            total_price += price
    print(f"Total price of fence for garden: {total_price}")


def part2(grid: Grid[str]) -> None:
    """
    ok... so...
    we need to keep track of the number of "sides" per "region" in the grid
    the "grid" is puzzle input data/day12.txt.

    Each letter represents a region.

    We want to calculate the total price for "fencing" every region.

    price_to_fence_region = number_of_sides_in_region * area

    gonna copy _some_ of part1 🫢
    """
    num_sides_cache = Grid[int | None].full_of(fill=None, size=len(grid))

    def cell_at_i_j_is_bridge(grid: Grid[str], i: int, j: int) -> bool:
        # cell at position grid[i][j] is a bridge (| |) if:
        # * it has exactly two sides
        # * and either:
        #   * the left and right neighbors are sides.
        #   * the top and bottom neighbors are sides.

        def is_side(item: Cell[str] | None) -> bool:
            return item is None or item.value != grid[i][j]

        left = grid.at((i - 1, j))
        right = grid.at((i + 1, j))
        top = grid.at((i, j - 1))
        bottom = grid.at((i, j + 1))
        side_count = sum(map(is_side, [left, right, top, bottom]))
        return side_count == 2 and (
            is_side(left) and is_side(right) or is_side(top) and is_side(bottom)
        )

    def get_outer_corner_count_at_cell_i_j(grid: Grid[str], i: int, j: int) -> int:
        perimeter = get_perimeter_at_cell_i_j(grid, i, j)
        if perimeter == 4:
            return 4
        if perimeter == 3:
            # this is a "peninsula". |_| <- that's 2 corners
            return 2
        if perimeter == 2:
            if cell_at_i_j_is_bridge(grid, i, j):
                # bridges have 2 sides, but no corners.
                # both of its sides will also appear
                # in other cells, so we don't count em
                return 0
            # it's a corner.
            return 1
        if perimeter <= 1:
            # it's either boundary-less or belongs to a boundary
            return 0
        raise ValueError(f"Invalid perimeter {perimeter}")

    def get_inner_corner_count_at_cell_i_j(grid: Grid[str], i: int, j: int) -> int:
        # an "inner corner" occurs whenever there exist two neighbors to (i, j)
        # that are diagonal to each other, but the cell diagonally adjacent to (i, j)
        # that is also next to those two neighbors is of a different region.
        inner_corner_count = 0
        for diagonal in grid.get_diagonals((i, j)):
            if diagonal.value != grid[i][j]:
                neighbor_edge_1 = grid.at((diagonal.i, j))
                neighbor_edge_2 = grid.at((i, diagonal.j))
                if (
                    neighbor_edge_1 is not None
                    and neighbor_edge_2 is not None
                    and neighbor_edge_1.value == grid[i][j]
                    and neighbor_edge_2.value == grid[i][j]
                ):
                    inner_corner_count += 1
        return inner_corner_count

    def find_region_number_of_sides_and_area(
        i: int, j: int, region_name: str
    ) -> tuple[int, int]:
        if grid[i][j] != region_name:
            return 0, 0
        outer_corner_count = get_outer_corner_count_at_cell_i_j(grid, i, j)
        inner_corner_count = get_inner_corner_count_at_cell_i_j(grid, i, j)
        number_of_sides = outer_corner_count + inner_corner_count
        num_sides_cache[i][j] = number_of_sides
        # print_grid_with_accent_at_i_j(num_sides_cache, i, j)
        # print_grid_with_accent_at_i_j(grid, i, j)
        # breakpoint()
        area = 1
        for cell in grid.get_nondiagonal_neighbors((i, j)):
            if cell.value == region_name and num_sides_cache[cell.i][cell.j] is None:
                cell_area, cell_num_sides = find_region_number_of_sides_and_area(
                    cell.i, cell.j, region_name
                )
                area += cell_area
                number_of_sides += cell_num_sides
        return area, number_of_sides

    total_price: int = 0
    for i, j, region in grid.traverse():
        if num_sides_cache[i][j] is None:
            area, num_sides = find_region_number_of_sides_and_area(i, j, region)
            price = area * num_sides
            # print(f"{region!r}: {area=} * {num_sides=} = {price}")
            # print_grid_with_accent_for_item(grid, region)
            # print(num_sides_cache)
            # breakpoint()
            total_price += price
    print(f"Total price of fence for garden: {total_price}")


if __name__ == "__main__":
    grid = Grid.for_day(12)
    test_grid = Grid.for_day(12, test_input=True)
    part1(grid)
    part2(grid)
