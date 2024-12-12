import sys
import time
from typing import Generator

def parse_file(filename: str) -> list[int]:
    with open(filename) as fp:
        digits = [int(d) for d in fp.read().strip().split(" ")]

    return digits


def solve_part1(puzzle_input: list[int]) -> int:

    def split_stones(digits: list[int]) -> list[int]:
        new_digits = []
        for d in digits:
            if d == 0:
                new_digits.append(1)
            elif (l := len(str(d))) % 2 == 0:
                mid = l // 2
                sd = str(d)
                left, right = sd[:mid], sd[mid:]
                new_digits.append(int(left))
                new_digits.append(int(right))
            else:
                new_digits.append(d * 2024)

        return new_digits


    digits = puzzle_input.copy()
    for _ in range(25):
        digits = split_stones(digits)

    return len(digits)


def solve_part2(puzzle_input: list[int]) -> int:

    def split_stone(digit: int, blinks: int) -> Generator[tuple[int,int],None,None]:
        if digit == 0:
            yield 1, blinks + 1
        elif len(str(digit)) % 2 == 0:
            sd = str(digit)
            mid = len(sd) // 2
            left, right = sd[:mid], sd[mid:]
            yield int(left), blinks + 1
            yield int(right), blinks + 1
        else:
            yield digit * 2024, blinks + 1


    digits = puzzle_input.copy()
    total_count = 0
    generator_stack = []
    for digit in digits:
        generator_stack.append(split_stone(digit, 0))

        while len(generator_stack):
            if ng := next(generator_stack[-1], None):
                d, blinks = ng
                if blinks == 75:
                    total_count += 1
                else:
                    generator_stack.append(split_stone(d, blinks))
            else:
                generator_stack.pop()

    return total_count


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

t0 = time.time()
sol1 = solve_part1(puzzle_input)
t1 = time.time()
print("part1:", sol1, f"(elapsed time: {t1 - t0:.4f}s)")

t0 = time.time()
sol2 = solve_part2(puzzle_input)
t1 = time.time()
print("part2:", sol2, f"(elapsed time: {t1 - t0:.4f}s)")

