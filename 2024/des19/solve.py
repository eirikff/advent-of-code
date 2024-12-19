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
    def check_pattern(pattern: str, depth: int = 0) -> bool:
        if (pattern, depth) in memo:
            return memo[(pattern, depth)]

        # We reached the end of the pattern meaning we found a match for each
        # substring
        if len(pattern) == 0:
            return True

        for i in range(len(pattern)):
            for j in range(min_length, max_length+1):
                sub = pattern[i:i+j]
                if sub in options:
                    success = check_pattern(pattern[j:], depth + 1)
                    if success:
                        memo[(pattern, depth)] = True
                        return True

            # If we can't match the start of the pattern, it automatically
            # fails
            memo[(pattern, depth)] = False
            return False

        raise RuntimeError(f"This should never be reached. {pattern=}, {options=}")


    total_count = 0
    for pattern in patterns:
        if check_pattern(pattern):
            total_count += 1

    return total_count


def solve_part2(options: set[str], patterns: list[str]) -> int:
    lengths = list(map(len, options))
    min_length = min(lengths)
    max_length = max(lengths)

    # def print(*args): pass

    memo = {}
    def find_combination(pattern: str, 
                         exclude_path: set[tuple] = set(), 
                         path: tuple = (), 
                         depth: int = 0) -> tuple[bool,tuple]:
        # Must use frozenset to make the exclude_path hashable
        arg_tuple = (pattern, frozenset(exclude_path), path, depth)
        if arg_tuple in memo:
            return memo[arg_tuple]

        # We reached the end of the pattern meaning we found a match for each
        # substring
        if len(pattern) == 0:
            return True, path

        for i in range(len(pattern)):
            for j in range(min_length, max_length+1):
                sub = pattern[i:i+j]
                if sub in options:
                    success, fullpath = find_combination(
                        pattern[j:], exclude_path, (*path, sub), depth + 1)
                    if success and fullpath not in exclude_path:
                        # print(f"[{depth}] {len(memo)}")
                        memo[arg_tuple] = (success, fullpath)
                        return success, fullpath

            memo[arg_tuple] = (False, ())
            return False, ()

        raise RuntimeError(f"This should never be reached. {pattern=}, {options=}, {exclude_path=}")


    def find_all(pattern: str) -> set[tuple]:
        paths = set()
        while True:
            success, path = find_combination(pattern, paths)
            if success:
                # print("found full path", path)
                paths.add(path)
            else:
                # print("impossible")
                break

        return paths


    total_count = 0
    for pattern in patterns:
        # print("\nTESTING PATTERN", pattern, "OPTIONS", options)
        print(pattern, end="", flush=True)
        paths = find_all(pattern)
        print("\tcount:", len(paths))
        total_count += len(paths)

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

