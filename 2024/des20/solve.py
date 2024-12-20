import sys
import time
from copy import deepcopy


START = "S"
END = "E"
WALL = "#"
TRACK = "."

ROWS = -1
COLS = -1


def within(row: int, col: int) -> bool:
    return row >= 0 and row < ROWS and col >= 0 and col < COLS


def parse_file(filename: str) -> list[list[str]]:
    global ROWS, COLS

    with open(filename) as fp:
        lines = fp.readlines()

    grid = [list(line.strip()) for line in lines]
    ROWS = len(grid)
    COLS = len(grid[0])
    return grid


def print_grid(grid: list[list[str]], 
               path: list[tuple[int,int]] = [],
               cheat: list[tuple[int,int]] = []):
    assert len(cheat) == 0 or len(cheat) == 2

    display = deepcopy(grid)
    for r, c in path:
        display[r][c] = "O"

    for i, (r, c) in enumerate(cheat):
        display[r][c] = str(i + 1)

    for row in display:
        print("".join(row))


def find_racetrack(grid: list[list[str]],
                   start: tuple[int,int],
                   end: tuple[int,int]
        ) -> tuple[list[tuple[int,int]],list[list[float]]]:
    # Find distances from start to each track cell
    distances = [ [ float("inf") ] * COLS for _ in range(ROWS) ]

    path = []
    node = start
    prev = (-1, -1)
    while node != end:
        r, c = node
        distances[r][c] = len(path)
        path.append(node)
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr = r + dr
            cc = c + dc
            if not within(rr, cc):
                continue

            if grid[rr][cc] == WALL:
                continue

            # Don't go backwards
            if (rr, cc) == prev:
                continue

            prev = node
            node = (rr, cc)
            break

    r, c = node
    distances[r][c] = len(path)
    path.append(node)

    return path, distances


def manhattan_distance(start: tuple[int,int], end: tuple[int,int]) -> int:
    return abs(end[0] - start[0]) + abs(end[1] - start[1])


def solve_part1(grid: list[list[str]]) -> int:
    start = (-1, -1)
    end = (-1, -1)
    for r in range(ROWS):
        for c in range(COLS):
            g = grid[r][c]
            if g == START:
                start = (r, c)
            elif g == END:
                end = (r, c)

    path, distances = find_racetrack(grid, start, end)

    save_counts = {}
    for i, (r, c) in enumerate(path):
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            # Cheat start
            r1 = r + dr
            c1 = c + dc
            # Cheat end
            r2 = r1 + dr
            c2 = c1 + dc
            if not within(r1, c1) or not within(r2, c2):
                continue

            # It doesn't make sense to disable collision if the first cell
            # is not a wall
            if grid[r1][c1] != WALL:
                continue

            # This ensures the second cheat is later in the path so we don't
            # cheat in a direction that doesn't make sense (e.g. the second
            # cheat is where we already have been
            if (r2, c2) not in path[i:]:
                continue

            dist_node = distances[r][c]
            dist_cheat_end = distances[r2][c2]
            cheat_length = 2
            save = dist_cheat_end - dist_node - cheat_length
            save_counts[save] = save_counts.get(save, 0) + 1

    total_count = 0
    for save, count in sorted(save_counts.items(), key=lambda i: i[0]):
        if save >= 100:
            total_count += count

    return total_count


def solve_part2(grid: list[list[str]]) -> int:
    start = (-1, -1)
    end = (-1, -1)
    for r in range(ROWS):
        for c in range(COLS):
            g = grid[r][c]
            if g == START:
                start = (r, c)
            elif g == END:
                end = (r, c)

    path, distances = find_racetrack(grid, start, end)

    save_counts = {}
    for i, node in enumerate(path):
        path_after = set(path[i:])

        for cheat_length in range(1, 21):
            cheat_ends = []
            for r in range(ROWS):
                for c in range(COLS):
                    if grid[r][c] == WALL:
                        continue

                    if (r, c) not in path_after:
                        continue

                    if manhattan_distance(node, (r, c)) == cheat_length:
                        cheat_ends.append((r, c))

            r, c = node
            for cheat_end in cheat_ends:
                r2, c2 = cheat_end
                dist_node = distances[r][c]
                dist_cheat_end = distances[r2][c2]
                save = dist_cheat_end - dist_node - cheat_length
                save_counts[save] = save_counts.get(save, 0) + 1

    total_count = 0
    for save, count in sorted(save_counts.items(), key=lambda i: i[0]):
        # print(f"There are {count} cheats that save {save} picoseconds.")
        if save >= 100:
            total_count += count

    return total_count


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

grid = parse_file(sys.argv[1])

t0 = time.time()
sol1 = solve_part1(deepcopy(grid))
t1 = time.time()
print("part1:", sol1, f"(elapsed time: {t1 - t0:.3f}s)")

t0 = time.time()
sol2 = solve_part2(deepcopy(grid))
t1 = time.time()
print("part2:", sol2, f"(elapsed time: {t1 - t0:.3f}s)")

