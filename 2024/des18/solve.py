import sys
from copy import deepcopy
import time
from typing import Callable

ROWS = 71
COLS = 71
MAX_BYTES = 1024

def parse_file(filename: str) -> list[tuple[int,int]]:
    with open(filename) as fp:
        lines = fp.readlines()

    coords = []
    for line in lines:
        x, y = line.split(",")
        # Reverse order to have coords be (row, col)
        coords.append((int(y), int(x)))

    return coords


def construct_grid(coords: list[tuple[int,int]]) -> list[list[str]]:
    grid = []
    for _ in range(ROWS):
        grid.append(["."] * COLS)

    for r, c in coords:
        grid[r][c] = "#"

    return grid


def print_grid(grid: list[list[str]], path: list[tuple[int,int]] = []):
    display = deepcopy(grid)
    for r, c in path:
        display[r][c] = "O"

    for row in display:
        print("".join(row))


def taxicab_distance(pos: tuple[int,int], end: tuple[int,int]) -> int:
    # Taxicab distance
    return abs(end[0] - pos[0]) + abs(end[1] - pos[1])


def a_star(start: tuple[int,int], 
           end: tuple[int,int], 
           grid: list[list[str]],
           heuristic: Callable[[tuple[int,int],tuple[int,int]],int]) -> list[tuple[int,int]]:
    # Implementation of A* from:
    # https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
    came_from = { start: None }
    # g_score = cheapest path from start to (r, c)
    g_score = [ [ float("inf") for _ in range(COLS) ] for __ in range(ROWS) ]
    # f_score = current best guess at how cheap path is from start to (r, c)
    f_score = [ [ float("inf") for _ in range(COLS) ] for __ in range(ROWS) ]

    r, c = start
    g_score[r][c] = 0
    f_score[r][c] = heuristic(start, end)

    def distance(current: tuple[int,int], neighbor: tuple[int,int]) -> int:
        return 1

    open_set = [start]
    while len(open_set) > 0:
        open_set = sorted(open_set, key=lambda n: f_score[n[0]][n[1]], reverse=True)
        current = open_set.pop()
        if current == end:
            prev = current
            path = [prev]
            while (prev := came_from[prev]) is not None:
                path.append(prev)

            return list(reversed(path))

        r, c = current
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            rr = r + dr
            cc = c + dc
            if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
                continue

            if grid[rr][cc] == "#":
                continue

            neighbor = (rr, cc)
            tentative_g_score = g_score[r][c] + distance(current, neighbor)
            if tentative_g_score < g_score[rr][cc]:
                came_from[neighbor] = current
                g_score[rr][cc] = tentative_g_score
                f_score[rr][cc] = tentative_g_score + heuristic(neighbor, end)

                if neighbor not in open_set:
                    open_set.append(neighbor)
    
    return []


def solve_part1(coords: list[tuple[int,int]], max_bytes: int = MAX_BYTES) -> int:
    grid = construct_grid(coords[:max_bytes])

    start = (0, 0)
    end = (ROWS - 1, COLS - 1)
    path = a_star(start, end, grid, taxicab_distance)

    # Subtract 1 because both start and end positions are included in the path
    return len(path) - 1


def solve_part2_linear_brute(coords: list[tuple[int,int]]) -> str:
    result = (-1,-1)
    for max_bytes in range(1024, len(coords)):
        path_length = solve_part1(coords, max_bytes=max_bytes)
        if path_length == -1:  # actual length = 0, but part1 subtracts 1 for start
            result = coords[max_bytes - 1]
            break

    # Reverse first block because coordinates are expected on form (col, row)
    return ",".join(str(d) for d in reversed(result))


def solve_part2_smart_brute(coords: list[tuple[int,int]]) -> str:
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)

    grid = construct_grid(coords[:MAX_BYTES])
    path = a_star(start, end, grid, taxicab_distance)

    result = (-1,-1)
    for max_bytes in range(1024, len(coords)):
        coord = coords[max_bytes]
        if coord not in path:
            continue

        grid = construct_grid(coords[:max_bytes])
        path = a_star(start, end, grid, taxicab_distance)

        if len(path) == 0:
            result = coords[max_bytes - 1]
            break

    # Reverse first block because coordinates are expected on form (col, row)
    return ",".join(str(d) for d in reversed(result))


def solve_part2_binary_search(coords: list[tuple[int,int]]) -> str:
    start = (0, 0)
    end = (ROWS - 1, COLS - 1)

    grid = construct_grid(coords[:MAX_BYTES])
    path = a_star(start, end, grid, taxicab_distance)

    result = (-1,-1)
    lower = 1024
    upper = len(coords)
    counter = -1
    while lower <= upper:
        counter += 1
        max_bytes = lower + (upper - lower) // 2
        grid = construct_grid(coords[:max_bytes])
        path = a_star(start, end, grid, taxicab_distance)

        if len(path) > 0:
            # This means the coord at max_bytes didn't block the path, so the
            # correct value is later in the coords list than at max_bytes
            lower = max_bytes + 1
        else:
            # This means the coord at max_bytes did block teh path, so the 
            # correct value is earlier in the coords list than at max_bytes
            upper = max_bytes - 1

    result = coords[lower - 1]

    # Reverse first block because coordinates are expected on form (col, row)
    return ",".join(str(d) for d in reversed(result))


def solve_part2(coords: list[tuple[int,int]]) -> str:
    # return solve_part2_linear_brute(coords)
    # return solve_part2_smart_brute(coords)
    return solve_part2_binary_search(coords)


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

coords = parse_file(sys.argv[1])

sol1 = solve_part1(coords)
print("part1:", sol1)

t0 = time.time()
sol2 = solve_part2(coords)
t1 = time.time()
print("part2:", sol2, f"(elapsed time: {t1 - t0:.4f}s)")

