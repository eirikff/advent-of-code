import sys
import itertools
import time

def parse_file(filename: str) -> list[tuple[int,list[int]]]:
    with open(filename) as fp:
        lines = fp.readlines()

    equations = []
    for line in lines:
        result, rest = line.split(":")
        numbers = [int(d.strip()) for d in rest.strip().split(" ")]

        equations.append((int(result), numbers))

    return equations


def test_possible(result: int, numbers: list[int], operators: list[str]) -> bool:
    holes = len(numbers) - 1
    perms = itertools.product(operators, repeat=holes)

    for perm in perms:
        number_stack = list(reversed(numbers))
        for op in perm:
            a, b = number_stack.pop(), number_stack.pop()
            if op == "+":
                number_stack.append(a + b)
            elif op == "*":
                number_stack.append(a * b)
            elif op == "||":
                number_stack.append(int(f"{a}{b}"))

        computed = number_stack[0]
        if computed == result:
            return True

    return False


def solve_part1(puzzle_input: list[tuple[int,list[int]]]) -> int:
    operators = ["+", "*"]

    total_sum = 0
    for result, numbers in puzzle_input:
        if test_possible(result, numbers, operators):
            total_sum += result

    return total_sum


def solve_part2(puzzle_input: list[tuple[int,list[int]]]) -> int:
    operators = ["+", "*", "||"]

    total_sum = 0
    for result, numbers in puzzle_input:
        if test_possible(result, numbers, operators):
            total_sum += result

    return total_sum


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

t0 = time.time()
sol1 = solve_part1(puzzle_input)
t1 = time.time()
print("part1:", sol1, f"{t1-t0:.4f}s")

t0 = time.time()
sol2 = solve_part2(puzzle_input)
t1 = time.time()
print("part2:", sol2, f"{t1-t0:.4f}s")

