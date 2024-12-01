import sys

def parse_file(filename: str) -> tuple[list[int], list[int]]:
    with open(filename) as fp:
        input_data = fp.readlines()

    input1, input2 = [], []
    for line in input_data:
        i, j = [int(d) for d in line.split(" ") if len(d)]
        input1.append(i)
        input2.append(j)

    return input1, input2

def solve_part1(input1: list[int], input2: list[int]) -> int:
    sorted1 = sorted(input1)
    sorted2 = sorted(input2)

    total_distance = 0
    for i, j in zip(sorted1, sorted2):
        dist = abs(i - j)
        total_distance += dist

    return total_distance


def solve_part2(input1: list[int], input2: list[int]) -> int:
    count = {}
    for j in input2:
        count[j] = count.get(j, 0) + 1

    total_similarity = 0
    for i in input1:
        multiplier = 0
        if i in count:
            multiplier = count[i]

        similarity = i * multiplier
        total_similarity += similarity

    return total_similarity


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

input1, input2 = parse_file(sys.argv[1])

total_distance = solve_part1(input1, input2)
print("part1:", total_distance)

total_similarity = solve_part2(input1, input2)
print("part2:", total_similarity)

