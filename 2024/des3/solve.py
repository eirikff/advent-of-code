import sys
import re

def parse_file(filename: str) -> str:
    with open(filename) as fp:
        content = fp.read()

    return content

def solve_part1(puzzle_input: str) -> int:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, puzzle_input)

    total = 0
    for a, b in matches:
        total += int(a) * int(b)

    return total


def solve_part2(puzzle_input: str) -> int:
    MUL_START = "mul("
    DO = "do()"
    DONT = "don't()"

    do_state = True
    instructions = []
    
    i = 0
    while i < len(puzzle_input):

        if puzzle_input[i:i+len(DO)] == DO:
            do_state = True
        elif puzzle_input[i:i+len(DONT)] == DONT:
            do_state = False
        elif puzzle_input[i:i+len(MUL_START)] == MUL_START:
            i += len(MUL_START)
            j = i
            while puzzle_input[j] in "0123456789,":
                j += 1

            # the mul expression must end with a closing parenthesis
            if puzzle_input[j] != ")":
                continue

            # subtract 1 because the closing parenthesis is included at j
            arguments = puzzle_input[i:j]
            a, b = arguments.split(",")
            instructions.append((do_state, int(a), int(b)))

        i += 1

    total = 0
    for do, a, b in instructions:
        if do:
            total += a * b

    return total


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

