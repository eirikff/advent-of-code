import sys

def parse_file(filename: str) -> None:
    pass

def solve_part1(puzzle_input: None) -> None:
    pass


def solve_part2(puzzle_input: None) -> None:
    pass


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

