import sys

def parse_file(filename: str) -> None:
    with open(filename) as fp:
        data = fp.read()

    pass


def solve_part1(puzzle_input: None) -> int:
    pass


def solve_part2(puzzle_input: None) -> int:
    pass


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

