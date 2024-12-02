import sys

def parse_file(filename: str) -> list[list[int]]:
    with open(filename) as fp:
        lines = fp.readlines()

    puzzle_input = []
    for line in lines:
        parsed = [int(d) for d in line.split(" ")]
        puzzle_input.append(parsed)

    return puzzle_input

def is_safe_line(line: list[int]) -> bool:
    # If the list is strictly increasing, the last number must be greater
    # than the first number.
    is_increasing = line[0] < line[-1]

    for i in range(len(line) - 1):
        a, b = line[i], line[i+1]
        
        if (is_increasing and b <= a) or (not is_increasing and b >= a):
            return False

        if abs(a - b) not in [1, 2, 3]:
            return False

    return True

def solve_part1(puzzle_input: list[list[int]]) -> int:
    safe_count = 0 
    for inp in puzzle_input:
        if is_safe_line(inp):
            safe_count += 1

    return safe_count


def solve_part2(puzzle_input: list[list[int]]) -> int:
    def is_safe_sub(line: list[int]) -> bool:
        for i in range(len(line)):
            sub_line = line[:i] + line[i+1:]
            if is_safe_line(sub_line):
                return True

        return False

    safe_count = 0 
    for inp in puzzle_input:
        if is_safe_sub(inp):
            safe_count += 1

    return safe_count


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

