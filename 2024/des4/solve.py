from os import PRIO_USER
import sys

def parse_file(filename: str) -> list[list[str]]:
    with open(filename) as fp:
        puzzle = [list(l.strip()) for l in fp.readlines()]

    return puzzle


def solve_part1(puzzle_input: list[list[str]]) -> int:
    xmas = list("XMAS")
    xmas_count = 0

    rows = len(puzzle_input)
    cols = len(puzzle_input[0])

    for r in range(rows):
        for c in range(cols):
            current = puzzle_input[r][c]

            # We only need to check places starting with X because we check in 
            # every direction.
            if current != "X":
                continue

            # right
            for i in range(4):
                if c + i >= cols: break
                if puzzle_input[r][c + i] != xmas[i]: break
            else:
                xmas_count += 1
            # left
            for i in range(4):
                if c - i < 0: break
                if puzzle_input[r][c - i] != xmas[i]: break
            else:
                xmas_count += 1
            # down
            for i in range(4):
                if r + i >= rows: break
                if puzzle_input[r + i][c] != xmas[i]: break
            else:
                xmas_count += 1
            # up
            for i in range(4):
                if r - i < 0: break
                if puzzle_input[r - i][c] != xmas[i]: break
            else:
                xmas_count += 1
            # diagonal down right
            for i in range(4):
                if r + i >= rows or c + i >= cols: break
                if puzzle_input[r + i][c + i] != xmas[i]: break
            else:
                xmas_count += 1
            # diagonal down left
            for i in range(4):
                if r + i >= rows or c - i < 0: break
                if puzzle_input[r + i][c - i] != xmas[i]: break
            else:
                xmas_count += 1
            # diagonal up right
            for i in range(4):
                if r - i < 0 or c + i >= cols: break
                if puzzle_input[r - i][c + i] != xmas[i]: break
            else:
                xmas_count += 1
            # diagonal up left
            for i in range(4):
                if r - i < 0 or c - i < 0: break
                if puzzle_input[r - i][c - i] != xmas[i]: break
            else:
                xmas_count += 1

    return xmas_count


def solve_part2(puzzle_input: list[list[str]]) -> int:
    xmas_count = 0

    rows = len(puzzle_input)
    cols = len(puzzle_input[0])

    for r in range(rows):
        for c in range(cols):
            current = puzzle_input[r][c]

            if current != "A":
                continue

            # Possible patterns
            #  (1)   (2)   (3)   (4)
            #  M M   M S   S S   S M
            #   A     A     A     A
            #  S S   M S   M M   S M

            # top left, top right, bot left, bot right
            indices = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            patterns = [
                ["M", "M", "S", "S"],  # (1)
                ["M", "S", "M", "S"],  # (2)
                ["S", "S", "M", "M"],  # (3)
                ["S", "M", "S", "M"],  # (4)
            ]
            
            for pattern in patterns:
                for i, (dr, dc) in enumerate(indices):
                    rr = r + dr
                    cc = c + dc 
                    if rr >= rows or rr < 0 or cc >= cols or cc < 0:
                        break

                    if puzzle_input[rr][cc] != pattern[i]:
                        break
                else:
                    xmas_count += 1

    return xmas_count


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

