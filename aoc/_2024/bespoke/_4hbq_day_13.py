import numpy as np
from rich import print

M = (
    np.fromregex(
        "data/day13.txt", r"\d+", [("", int)] * 6
    )  # load data into array of sextuples
    .view(int)  # flatten and convert to int
    .reshape(-1, 3, 2)  # reshape to 3x2 array
    .swapaxes(1, 2)  # swap axes to match the equation
)


def part1(extra_stuff_to_add_to_prize_coordinates: float = 0) -> None:
    S = M[..., :2]
    P = M[..., 2:] + extra_stuff_to_add_to_prize_coordinates
    R = np.linalg.solve(S, P).round().astype(int)
    print(
        "[bold green] numpy_solution total cost[/bold green]:",
        *R.squeeze() @ [3, 1] @ (S @ R == P).all(1),
    )


def part2() -> None:
    part1(extra_stuff_to_add_to_prize_coordinates=1e13)


if __name__ == "__main__":
    part1()
    part2()
