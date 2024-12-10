import sys

def parse_file(filename: str) -> list[list[int]]:
    with open(filename) as fp:
        lines = fp.readlines()

    topo = []
    for line in lines:
        topo.append([int(d) for d in line.strip()])

    return topo


def solve_part1(topo: list[list[int]]) -> int:
    rows = len(topo)
    cols = len(topo[0])

    def find_trail_ends(start: tuple[int,int]) -> set[tuple[int,int]]:
        r, c = start
        
        if topo[r][c] == 9:
            return {(r, c)}

        ends = set()
        for dr, dc in [ (-1, 0), (0, -1), (1, 0), (0, 1), ]:
            rr = r + dr
            cc = c + dc
            
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                continue

            if topo[rr][cc] == topo[r][c] + 1 and (rr, cc) not in ends:
                ends = ends | find_trail_ends((rr, cc))

        return ends


    trail_count = 0
    for r in range(rows):
        for c in range(cols):
            if topo[r][c] == 0:
                ends = find_trail_ends((r, c))
                trail_count += len(ends)

    return trail_count


def solve_part2(topo: list[list[int]]) -> int:
    rows = len(topo)
    cols = len(topo[0])

    def find_unique_trails(start: tuple[int,int]) -> int:
        r, c = start
        
        if topo[r][c] == 9:
            return 1

        count = 0
        for dr, dc in [ (-1, 0), (0, -1), (1, 0), (0, 1), ]:
            rr = r + dr
            cc = c + dc
            
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                continue

            if topo[rr][cc] == topo[r][c] + 1:
                count += find_unique_trails((rr, cc))

        return count


    trail_count = 0
    for r in range(rows):
        for c in range(cols):
            if topo[r][c] == 0:
                count = find_unique_trails((r, c))
                trail_count += count

    return trail_count


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

