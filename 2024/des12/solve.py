from __future__ import annotations
import sys
from copy import deepcopy

def parse_file(filename: str) -> list[list[str]]:
    with open(filename) as fp:
        grid = [list(line.strip()) for line in fp.readlines()]

    return grid


class DirectedEdge:
    def __init__(self, start: tuple[int,int], end: tuple[int,int]):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{self.start}->{self.end}"

    def opposite(self, other: DirectedEdge) -> bool:
        return self.start == other.end and self.end == other.start


class GardenPlot:
    def __init__(self, cells: set[tuple[int,int]], label: str = ""):
        self.cells = deepcopy(cells)
        self.label = label
        self.find_outline()

    def __repr__(self):
        return f"Plot(label={repr(self.label)}, area={self.area()}, cells={' '.join(str(c) for c in self.cells)})"

    def area(self) -> int:
        return len(self.cells)

    def perimeter(self) -> int:
        assert self.outline is not None, \
            "Must call GardenPlot.find_outline before computing the perimeter"
        return len(self.outline)

    def sides(self) -> int:
        # TODO: for part 2
        return -1

    def cost(self) -> int:
        return self.area() * self.perimeter()

    def bulk_cost(self) -> int:
        return self.area() * self.sides()

    def contains(self, cell: tuple[int,int]) -> bool:
        return cell in self.cells

    def find_outline(self) -> list[DirectedEdge]:
        def cell_edges(cell: tuple[int,int]) -> list[DirectedEdge]:
            r, c = cell
            vectors = []
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                rr = r + dr
                cc = c + dc
                vectors.append(DirectedEdge((r, c), (rr, cc)))
                r = rr
                c = cc

            return vectors

        edges = [edge for cell in self.cells for edge in cell_edges(cell)]

        self.outline = []
        for edge in edges:
            for other in edges:
                if edge.opposite(other):
                    break
            else:
                self.outline.append(edge)

        return self.outline


def floodfill(start: tuple[int,int], grid: list[list[str]]) -> GardenPlot:
    # Breath first search for a region
    sr, sc = start
    letter = grid[sr][sc]

    rows = len(grid)
    cols = len(grid[0])

    garden_plot = set()
    queue = [(sr, sc)]
    while len(queue):
        r, c = queue.pop(0)
        # Need to use a set because the last cell can sometimes be added
        # multiple times to the queue
        garden_plot.add((r, c))
        
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            rr = r + dr
            cc = c + dc
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                continue

            cell = (rr, cc)
            not_in_queue = cell not in queue
            not_in_garden = cell not in garden_plot
            if grid[rr][cc] == letter and not_in_garden and not_in_queue:
                queue.append((rr, cc))
            
    return GardenPlot(garden_plot, label=letter)


def solve_part1(garden: list[list[str]]) -> int:
    rows = len(garden)
    cols = len(garden[0])

    total_cost = 0
    plots = []
    for r in range(rows):
        for c in range(cols):
            for plot in plots:
                if plot.contains((r, c)):
                    break
            else:
                plot = floodfill((r,c), garden)
                plots.append(plot)
                total_cost += plot.cost()

    return total_cost


def solve_part2(garden: list[list[str]]) -> int:
    rows = len(garden)
    cols = len(garden[0])

    total_cost = 0
    plots = []
    for r in range(rows):
        for c in range(cols):
            for plot in plots:
                if plot.contains((r, c)):
                    break
            else:
                plot = floodfill((r,c), garden)
                plots.append(plot)
                total_cost += plot.bulk_cost()

    return total_cost


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

