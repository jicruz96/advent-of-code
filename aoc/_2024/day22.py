import itertools
from collections import defaultdict
from typing import Generator

from aoc.helpers import get_input_text


def evolve_secret(secret: int) -> int:
    secret = prune(mix(secret, secret * (2**6)))
    secret = prune(mix(secret, secret // (2**5)))
    secret = prune(mix(secret, secret * (2**11)))
    return secret


def mix(secret: int, res: int) -> int:
    return res ^ secret


def prune(secret: int) -> int:
    return secret % 16_777_216


def produce_secrets(secret: int, n: int) -> list[int]:
    secrets = [secret]
    for _ in range(n):
        secret = evolve_secret(secret)
        secrets.append(secret)
    return secrets


def iter_input_secrets() -> Generator[int]:
    yield from map(int, get_input_text(22).splitlines())


def part1() -> None:
    sum_of_2000th_secret_number = sum(
        produce_secrets(secret, 2_000)[-1] for secret in iter_input_secrets()
    )
    print(f"{sum_of_2000th_secret_number=}")


def sliding_window(arr: list[int], size: int) -> Generator[list[int]]:
    for i in range(len(arr) - size + 1):
        yield arr[i : i + size]


def part2() -> None:
    cache: dict[tuple[int, ...], dict[int, int]] = defaultdict(dict)
    for secret in iter_input_secrets():
        secrets = produce_secrets(secret, 2_000)
        bananas = [int(str(secret)[-1]) for secret in secrets]
        deltas = [prev - curr for prev, curr in itertools.pairwise(bananas)]
        for i, combination in enumerate(map(tuple, sliding_window(deltas, 4))):
            if secret not in cache[combination]:
                cache[combination][secret] = bananas[i + 4]

    max_combo = (0, 0, 0, 0)
    max_value = 0
    for combo, combo_cache in cache.items():
        bananas = sum(combo_cache.values())
        if bananas > max_value:
            max_value = bananas
            max_combo = combo

    print(f"{max_combo=} {max_value=}")


if __name__ == "__main__":
    part2()
