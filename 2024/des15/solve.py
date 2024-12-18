import sys
from copy import deepcopy
import time

ROBOT = "@"

# For part 1
WALL = "#"
BOX = "O"
EMPTY = "."

# For part 2
WALL2 = "##"
BOX2 = "[]"
EMPTY2 = ".."

LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"


def parse_file(filename: str) -> tuple[list[list[str]],list[str]]:
    with open(filename) as fp:
        data = fp.read()

    grid_in, moves_in = data.split("\n\n")

    grid = []
    for i, line in enumerate(grid_in.splitlines()):
        grid.append([])
        for c in line:
            grid[i].append(c)

    moves = []
    for m in moves_in:
        if m == "\n":
            continue
        moves.append(m)

    return grid, moves


def within(row: int, col: int, rows: int, cols: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


def print_grid(grid: list[list[str]]):
    print("\n".join("".join(row) for row in grid))


def move_to_dir(m: str) -> tuple[int,int]:
    if m == LEFT:
        dir = (0, -1)
    elif m == RIGHT:
        dir = (0, 1)
    elif m == UP:
        dir = (-1, 0)
    elif m == DOWN:
        dir = (1, 0)
    else:
        raise ValueError(f"Move '{m}' is invalid")

    return dir


def solve_part1(grid: list[list[str]], moves: list[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    robot = (-1, -1)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == ROBOT:
                robot = (r, c)

    def move(robot: tuple[int,int], m: str) -> tuple[int,int]:
        r, c = robot
        grid[r][c] = EMPTY

        dr, dc = move_to_dir(m)

        rr = r + dr
        cc = c + dc
        if not within(rr, cc, rows, cols):
            grid[r][c] = ROBOT
            return r, c

        if grid[rr][cc] == WALL:
            grid[r][c] = ROBOT
            return r, c

        if grid[rr][cc] == BOX:
            # Find first non-box cell
            rb = rr
            cb = cc
            while within(rb, cb, rows, cols) and grid[rb][cb] == BOX:
                rb = rb + dr
                cb = cb + dc

            if grid[rb][cb] == WALL:
                grid[r][c] = ROBOT
                return r, c

            # Move box to the next empty cell. This is the same as moving each
            # box since the boxes are identical. 
            grid[rr][cc] = EMPTY
            grid[rb][cb] = BOX

        r = rr
        c = cc

        grid[r][c] = ROBOT
        return r, c

    for m in moves:
        robot = move(robot, m)

    sum_position = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == BOX:
                pos = 100 * r + c
                sum_position += pos

    return sum_position


def solve_part2(grid_pt1: list[list[str]], moves: list[str]) -> int:
    # Prepare for part 2
    rows = len(grid_pt1)
    cols = len(grid_pt1[0])
    robot = (-1, -1)
    for r in range(rows):
        for c in range(cols):
            g = grid_pt1[r][c]
            if g == WALL:
                grid_pt1[r][c] = WALL2
            elif g == BOX:
                grid_pt1[r][c] = BOX2
            elif g == EMPTY:
                grid_pt1[r][c] = EMPTY2
            elif g == ROBOT:
                grid_pt1[r][c] = ROBOT + EMPTY

                # Multiply column with two since each cell is double length now
                robot = (r, c * 2)

    # Expand grid so each double cell is it's own item
    grid = []
    for i, row in enumerate(grid_pt1):
        grid.append([])
        for cell in row:
            grid[i].append(cell[0])
            grid[i].append(cell[1])

    rows = len(grid)
    cols = len(grid[0])

    print_grid(grid)
    print("robot init", robot)

    def move(robot: tuple[int,int], m: str) -> tuple[int,int]:
        r, c = robot
        grid[r][c] = EMPTY

        dr, dc = move_to_dir(m)
        print("\nmove", m, dr, dc)

        rr = r + dr
        cc = c + dc
        if not within(rr, cc, rows, cols):
            grid[r][c] = ROBOT
            print("outside", rr, cc)
            return r, c

        if grid[rr][cc] == WALL:
            grid[r][c] = ROBOT
            print("wall", rr, cc)
            return r, c

        if grid[rr][cc] in BOX2:
            print("box", rr, cc)
            if m in [LEFT, RIGHT]:
                # Find first non-box cell
                rb = rr
                cb = cc
                while within(rb, cb, rows, cols) and grid[rb][cb] in BOX2:
                    rb = rb + dr
                    cb = cb + dc

                print("found not box", rb, cb)

                if grid[rb][cb] == WALL:
                    grid[r][c] = ROBOT
                    return r, c

                print("found empty", rb, cb)

                while rb != r or cb != c:
                    tmp = grid[rb][cb]
                    grid[rb][cb] = grid[rb + dr][cb + dc]
                    grid[rb + dr][cb + dc] = tmp
                    rb -= dr
                    cb -= dc

            elif m in [UP, DOWN]:
                # IDEAS
                # There are two cases: (robot can be under either side)
                #   1) where two boxes are directly under each other, ie:
                #       []
                #       []
                #       @.
                #   2) where they are shifted one (like the example). 
                #       [].
                #       .[]
                #       ..@
                # 
                # Search up directly above robot and one to the side (depending
                # on which side the robot is on). If a new box is found, expand 
                # the search for both sides of the new box. This will be kind of
                # like a DFS. 
                #
                # Can have examples that are something like this:
                #   ..........
                #   ..[]......
                #   ...[][]...
                #   ....[]....
                #   .....[]...
                #   ......[]..
                #   .......[].
                #   ........@.
                # In which case the robot will move all boxes up one. 
                pass

        r = rr
        c = cc

        grid[r][c] = ROBOT
        return r, c

    for m in moves[:5]:
        robot = move(robot, m)

    print("before up")
    print_grid(grid)

    for m in moves[5:7]:
        robot = move(robot, m)

    print("final")
    print_grid(grid)

    return -1

if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

grid, moves = parse_file(sys.argv[1])

sol1 = solve_part1(deepcopy(grid), moves)
print("part1:", sol1)

sol2 = solve_part2(deepcopy(grid), moves)
print("part2:", sol2)

