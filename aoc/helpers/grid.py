from __future__ import annotations

from typing import Callable, Generator, Literal, NamedTuple, TypeAlias, overload

from .input import get_input_as_grid

Direction: TypeAlias = Literal["left", "right", "top", "bottom"]


class NotGiven:
    pass


NOT_GIVEN: NotGiven = NotGiven()


class Cell[T = str](NamedTuple):
    i: int
    j: int
    value: T

    @property
    def coords(self) -> tuple[int, int]:
        return (self.i, self.j)

    @property
    def left_coords(self) -> tuple[int, int]:
        return (self.i, self.j - 1)

    @property
    def right_coords(self) -> tuple[int, int]:
        return (self.i, self.j + 1)

    @property
    def up_coords(self) -> tuple[int, int]:
        return self.i - 1, self.j

    @property
    def down_coords(self) -> tuple[int, int]:
        return self.i + 1, self.j

    @overload
    def neighbor_type(self, neighbor: Cell[T], strict: Literal[True]) -> Direction: ...
    @overload
    def neighbor_type(
        self, neighbor: Cell[T], strict: bool = False
    ) -> Direction | None: ...

    def neighbor_type(
        self, neighbor: Cell[T], strict: bool = False
    ) -> Direction | None:
        lateral_distance = abs(neighbor.i - self.i) + abs(neighbor.j - self.j)
        if lateral_distance != 1:
            if strict:
                raise ValueError(f"Cell {neighbor} is not a neighbor of {self}")
            return None
        if self.i == neighbor.i:
            return "right" if neighbor.j > self.j else "left"
        return "bottom" if neighbor.i > self.i else "top"


class Grid[T = str]:
    def __init__(
        self,
        grid: list[list[T]],
    ) -> None:
        self.__grid = grid

    @classmethod
    def from_string(cls, s: str) -> Grid[str]:
        return cls(list(map(list, s.splitlines())))  # type: ignore

    @classmethod
    def full_of(
        cls,
        fill: T | Callable[[], T],
        size: int | tuple[int, int],
    ) -> Grid[T]:
        if isinstance(size, int):
            size = (size, size)
        i, j = size
        if callable(fill):
            return cls([[fill() for _ in range(j)] for _ in range(i)])  # type: ignore
        return cls([[fill for _ in range(j)] for _ in range(i)])

    def __len__(self) -> int:
        return len(self.__grid)

    def __repr__(self) -> str:
        text = ""
        for x in range(len(self)):
            for y in range(len(self[x])):
                value = self[x][y]
                if value is None:
                    value = "."
                else:
                    value = str(value)
                text += value
            text += "\n"
        return text

    @overload
    def __getitem__(self, item: int) -> list[T]: ...

    @overload
    def __getitem__(self, item: slice[int]) -> list[list[T]]: ...

    def __getitem__(self, item: int | slice[int]) -> list[T] | list[list[T]]:
        return self.__grid[item]

    def __setitem__(self, item: int, thing: T) -> None:
        self[item] = thing

    @overload
    def at(self, coords: tuple[int, int], *, strict: Literal[True]) -> Cell[T]: ...

    @overload
    def at(
        self, coords: tuple[int, int], *, strict: bool = False
    ) -> Cell[T] | None: ...

    def at(self, coords: tuple[int, int], *, strict: bool = False) -> Cell[T] | None:
        if self.is_off_grid(coords):
            if strict:
                raise ValueError(f"Coords{coords} are out of bounds")
            return None
        return Cell(i=coords[0], j=coords[1], value=self[coords[0]][coords[1]])

    def is_off_grid(self, coords: tuple[int, int]) -> bool:
        x, y = coords
        return len(self) == 0 or x < 0 or x >= len(self) or y < 0 or y >= len(self[0])

    def traverse(self) -> Generator[Cell[T]]:
        for i in range(len(self)):
            for j in range(len(self[i])):
                yield Cell(i, j, self[i][j])

    @overload
    def first(self, item: T, strict: Literal[True]) -> Cell[T]: ...
    @overload
    def first(self, item: T, strict: bool = False) -> Cell[T] | None: ...

    def first(self, item: T, strict: bool = False) -> Cell[T] | None:
        for cell in self.traverse():
            if cell.value == item:
                return cell
        if strict:
            raise ValueError(f"item {item!r} not in grid {self}")

    def get_diagonals(
        self,
        coords: tuple[int, int],
    ) -> list[Cell[T]]:
        i, j = coords
        return [
            Cell(i=x, j=y, value=self[x][y])
            for (x, y) in [
                (i - 1, j - 1),  # top-left diagonal
                (i - 1, j + 1),  # top-right diagonal
                (i + 1, j - 1),  # bottom-left diagonal
                (i + 1, j + 1),  # bottom-right diagonal
            ]
            if not self.is_off_grid((x, y))
        ]

    def get_nondiagonal_neighbors(
        self,
        coords: tuple[int, int],
    ) -> list[Cell[T]]:
        i, j = coords
        return [
            Cell(i=x, j=y, value=self[x][y])
            for (x, y) in [
                (i - 1, j),  # left
                (i + 1, j),  # right
                (i, j + 1),  # top
                (i, j - 1),  # bottom
            ]
            if not self.is_off_grid((x, y))
        ]

    def print_with_accent_at_i_j(self, i: int, j: int) -> None:
        from rich import print

        text = ""
        for x in range(len(self)):
            for y in range(len(self[x])):
                value = self[x][y]
                if x == i and y == j:
                    value = f"[bold blue]{value}[/bold blue]"
                elif value is None:
                    value = "."
                else:
                    value = str(value)
                text += value
            text += "\n"
        print(text)

    def print_with_accent_for_item(self, item: T) -> None:
        from rich import print

        text = ""
        for x in range(len(self)):
            for y in range(len(self[x])):
                value = self[x][y]
                if value == item:
                    value = f"[bold blue]{value}[/bold blue]"
                elif value is None:
                    value = "."
                else:
                    value = str(value)
                text += value
            text += "\n"
        print(text)

    @classmethod
    def for_day(cls, day: int, *, test_input: bool = False) -> Grid[str]:
        return cls(get_input_as_grid(day, test_input=test_input))  # type: ignore

    @property
    def size(self) -> tuple[int, int]:
        return (len(self), len(self[0]) if len(self) else 0)
