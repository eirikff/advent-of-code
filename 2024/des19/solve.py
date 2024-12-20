import sys
import time

def parse_file(filename: str) -> tuple[set[str],list[str]]:
    with open(filename) as fp:
        lines = fp.readlines()

    options = set(line.strip() for line in lines[0].split(", "))
    patterns = [line.strip() for line in lines[2:]]

    return options, patterns


def solve_part1(options: set[str], patterns: list[str]) -> int:
    lengths = list(map(len, options))
    min_length = min(lengths)
    max_length = max(lengths)

    memo = {}
    def check_pattern(pattern: str) -> bool:
        if pattern in memo:
            return memo[pattern]

        # We reached the end of the pattern meaning we found a match for each
        # substring
        if len(pattern) == 0:
            return True

        for j in range(min_length, max_length+1):
            sub = pattern[:j]
            if sub in options:
                success = check_pattern(pattern[j:])
                if success:
                    memo[pattern] = True
                    return True

        # If we can't match the start of the pattern, it automatically
        # fails
        memo[pattern] = False
        return False


    total_count = 0
    for pattern in patterns:
        if check_pattern(pattern):
            total_count += 1

    return total_count


def solve_part2(options: set[str], patterns: list[str]) -> int:
    memo = {}
    def find_count(pattern: str, path: tuple = ()) -> int:
        # We reached the end of the pattern meaning we found a match for each
        # substring
        if len(pattern) == 0:
            return 1

        if pattern in memo:
            return memo[pattern]

        count = 0
        for sub in options:
            if pattern.startswith(sub):
                j = len(sub)
                count += find_count(pattern[j:], (*path, sub))

        memo[pattern] = count
        return count


    total_count = 0
    for pattern in patterns:
        count = find_count(pattern)
        total_count += count

    return total_count


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

options, patterns = parse_file(sys.argv[1])

t0 = time.time()
sol1 = solve_part1(options, patterns)
t1 = time.time()
print("part1:", sol1, f"(elapsed time: {t1 - t0:.4f})s")

t0 = time.time()
sol2 = solve_part2(options, patterns)
t1 = time.time()
print("part2:", sol2, f"(elapsed time: {t1 - t0:.4f})s")

