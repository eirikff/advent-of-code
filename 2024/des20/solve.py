import sys
import time
from copy import deepcopy
from typing import Callable


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


def djikstra(grid: list[list[str]], 
             start: tuple[int,int], 
             target: tuple[int,int]):
    distances = {}
    previous = {}
    open_set = []

    for r in range(ROWS):
        for c in range(COLS):
            distances[(r, c)] = float("inf")
            previous[(r, c)] = None
            open_set.append((r, c))

    distances[start] = 0

    while len(open_set) > 0:
        open_set.sort(key=lambda n: distances[n], reverse=True)
        candidate = open_set.pop()
        if candidate == target:
            path = []
            while candidate is not None:
                path.append(candidate)
                candidate = previous[candidate]
            return list(reversed(path))

        r, c = candidate
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr = r + dr
            cc = c + dc
            if not within(rr, cc):
                continue

            neighbor = (rr, cc)
            if grid[rr][cc] == WALL:
                continue

            neighbor_dist = distances[candidate] + 1
            if neighbor_dist < distances[neighbor]:
                distances[neighbor] = neighbor_dist
                previous[neighbor] = candidate

    return []


def taxicab_distance(pos: tuple[int,int], end: tuple[int,int]) -> int:
    # Taxicab distance
    return abs(end[0] - pos[0]) + abs(end[1] - pos[1])


def a_star(grid: list[list[str]],
           start: tuple[int,int], 
           end: tuple[int,int], 
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

    # path = djikstra(grid, start, end)
    path = a_star(grid, start, end, taxicab_distance)

    cheats = []
    for i, (r, c) in enumerate(path):
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            r1 = r + dr
            c1 = c + dc
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

            cheat = [
                (r1, c1),
                (r2, c2),
            ]
            cheats.append(cheat)

    save_counts = {}
    for cheat in cheats:
        old = {}
        for r, c in cheat:
            old[(r, c)] = grid[r][c]
            grid[r][c] = TRACK

        # new_path = djikstra(grid, start, end)
        new_path = a_star(grid, start, end, taxicab_distance)
        save = len(path) - len(new_path)
        if save > 0:
            save_counts[save] = save_counts.get(save, 0) + 1

        for r, c in cheat:
            grid[r][c] = old[(r, c)]

    total_count = 0
    for save, count in sorted(save_counts.items(), key=lambda i: i[0]):
        if save >= 100:
            total_count += count

    return total_count


def solve_part2(grid: list[list[str]]) -> int:
    pass


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

grid = parse_file(sys.argv[1])

sol1 = solve_part1(deepcopy(grid))
print("part1:", sol1)

sol2 = solve_part2(deepcopy(grid))
print("part2:", sol2)

