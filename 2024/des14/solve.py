import sys
from copy import deepcopy
from PIL import Image


class Robot:
    def __init__(self, px: int, py: int, vx: int, vy: int):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def step(self, rows: int, cols: int):
        self.px = (self.px + self.vx) % cols
        self.py = (self.py + self.vy) % rows

    @property
    def r(self):
        return self.py

    @property
    def c(self):
        return self.px


def parse_file(filename: str) -> tuple[list[Robot],int,int]:
    with open(filename) as fp:
        lines = fp.readlines()

    w, h = lines[0].split(" ")
    rows = int(h[2:])
    cols = int(w[2:])

    robots = []
    for line in lines[1:]:
        pos, vel = line.split(" ")
        px, py = [int(d) for d in pos[2:].split(",")]
        vx, vy = [int(d) for d in vel[2:].split(",")]
        robots.append(Robot(px, py, vx, vy))

    return robots, rows, cols


def print_grid(robots: list[Robot], rows: int, cols: int, *, middle_char: str = "*"):
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            grid[r].append(0)

    for robot in robots:
        grid[robot.r][robot.c] += 1

    middle_row = rows // 2
    middle_col = cols // 2

    output = ""
    for r in range(rows):
        for c in range(cols):
            if (count := grid[r][c]) > 0:
                output += str(count)
            else:
                if r == middle_row or c == middle_col:
                    output += middle_char
                else:
                    output += "."
        output += "\n"

    print(output)


def solve_part1(robots: list[Robot], rows: int, cols: int) -> int:
    for _ in range(100):
        for robot in robots:
            robot.step(rows, cols)

    middle_row = rows // 2
    middle_col = cols // 2

    quadrants_count = [0, 0, 0, 0]
    for robot in robots:
        if robot.r == middle_row or robot.c == middle_col:
            continue
        
        row = 0 if robot.r < middle_row else 1
        col = 0 if robot.c < middle_col else 1
        idx = row * 2 + col
        quadrants_count[idx] += 1

    safety_factor = 1
    for q in quadrants_count:
        safety_factor *= q

    return safety_factor


def solve_part2(robots: list[Robot], rows: int, cols: int) -> int:
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            grid[r].append(0)

    sec = 0
    while sec < 20000:
        for robot in robots:
            robot.step(rows, cols)
        sec += 1

        for robot in robots:
            grid[robot.r][robot.c] += 1

        # Assuming the chirstmas tree has some consecutive pixels in the
        # horizontal direction. When the number of consecutive pixels reaches a
        # threshold, we assume we have found the tree. 
        # Another way is to compute the entropy of the map and select the one
        # with the lowest entropy. The consecutive pixel count method kinda
        # does this, but with a questionable heuristic. 
        # One entropy measure could be the safety factor from part 1. 
        consecutive_count = 0

        img_bytes = b""
        found = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] > 0:
                    img_bytes += b"\xff"
                    consecutive_count += 1
                else:
                    img_bytes += b"\x00"
                    consecutive_count = 0

                # Reset for next iteration
                grid[r][c] = 0

                if consecutive_count > 20:
                    found = True

        if found:
            img = Image.new("L", (cols, rows))  # mode L = 8-bit grayscale
            img.frombytes(img_bytes)
            img.save(f"{sec}.png")

            return sec

    return -1


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

robots, rows, cols = parse_file(sys.argv[1])

sol1 = solve_part1(deepcopy(robots), rows, cols)
print("part1:", sol1)

sol2 = solve_part2(deepcopy(robots), rows, cols)
print("part2:", sol2)

