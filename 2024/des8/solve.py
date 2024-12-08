import sys
import itertools
from copy import deepcopy

def parse_file(filename: str) -> list[list[str]]:
    with open(filename) as fp:
        lines = fp.readlines()

    board = [list(line.strip()) for line in lines]
    return board


def vector_add(v1: tuple[int,int], v2: tuple[int,int]) -> tuple[int,int]:
    return (
        v1[0] + v2[0],
        v1[1] + v2[1],
    )


def vector_sub(v1: tuple[int,int], v2: tuple[int,int]) -> tuple[int,int]:
    return (
        v1[0] - v2[0],
        v1[1] - v2[1],
    )


def vector_mul(v: tuple[int,int], s: int) -> tuple[int,int]:
    return (
        s * v[0],
        s * v[1],
    )


def solve_part1(puzzle_input: list[list[str]]) -> int:
    puzzle_map = deepcopy(puzzle_input)
    rows = len(puzzle_map)
    cols = len(puzzle_map[0])

    frequencies = {}
    for r in range(rows):
        for c in range(cols):
            f = puzzle_map[r][c]
            if f not in ["."]:
                frequencies[f] = frequencies.get(f, []) + [(r, c)]

    valid_anitnodes = set()
    for freq, poles in frequencies.items():
        antinodes = set()
        for pole1, pole2 in itertools.product(poles, poles):
            if pole1 == pole2:
                continue

            delta = vector_sub(pole2, pole1)

            anti1 = vector_sub(pole1, delta)
            anti2 = vector_add(pole2, delta)

            antinodes.add(anti1)
            antinodes.add(anti2)

        for r, c in antinodes:
            if r >= rows or r < 0 or c >= cols or c < 0:
                continue

            # We count all antinodes within the bounds of the map, even if it
            # overlaps with another frequency
            valid_anitnodes.add((r, c))

            # But we only visualize the ones that don't overlap
            if puzzle_map[r][c] != ".":
                continue

            puzzle_map[r][c] = "#"

    print("Part 1 antinodes:")
    for row in puzzle_map:
        print("".join(row))

    return len(valid_anitnodes)


def solve_part2(puzzle_input: list[list[str]]) -> int:
    puzzle_map = deepcopy(puzzle_input)
    rows = len(puzzle_map)
    cols = len(puzzle_map[0])

    def within(row: int, col: int) -> bool:
        return row < rows and row >= 0 and col < cols and col >= 0

    frequencies = {}
    for r in range(rows):
        for c in range(cols):
            f = puzzle_map[r][c]
            if f not in ["."]:
                frequencies[f] = frequencies.get(f, []) + [(r, c)]

    valid_anitnodes = set()
    for freq, poles in frequencies.items():
        antinodes = set()
        for pole1, pole2 in itertools.product(poles, poles):
            if pole1 == pole2:
                continue

            delta = vector_sub(pole2, pole1)

            scalar = 0
            while True:
                anti = vector_sub(pole1, vector_mul(delta, scalar))
                if not within(*anti):
                    break
                antinodes.add(anti)
                scalar += 1

            scalar = 0
            while True:
                anti = vector_add(pole2, vector_mul(delta, scalar))
                if not within(*anti):
                    break
                antinodes.add(anti)
                scalar += 1


        for r, c in antinodes:
            if not within(r, c):
                continue

            # We count all antinodes within the bounds of the map, even if it
            # overlaps with another frequency
            valid_anitnodes.add((r, c))

            # But we only visualize the ones that don't overlap
            if puzzle_map[r][c] != ".":
                continue

            puzzle_map[r][c] = "#"

    print("Part 2 antinodes:")
    for row in puzzle_map:
        print("".join(row))

    return len(valid_anitnodes)


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])
print("Input:")
for row in puzzle_input:
    print("".join(row))

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

