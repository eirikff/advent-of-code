import sys

def parse_file(filename: str) -> tuple[list[tuple[int,int]], list[list[int]]]:
    with open(filename) as fp:
        lines = fp.readlines()

    rules = []

    line_index = 0
    while line_index < len(lines):
        line = lines[line_index].strip()
        if line == "":
            # End of rules
            line_index += 1
            break

        a, b = line.split("|")
        rules.append((int(a), int(b)))
        line_index += 1

    pages = []
    while line_index < len(lines):
        numbers = lines[line_index].split(",")
        pages.append(list(int(p) for p in numbers))
        line_index += 1

    return rules, pages


def solve_part1(rules: list[tuple[int,int]], pages: list[list[int]]) -> int:
    def check_valid_order(update: list[int]) -> bool:
        for i in range(len(update)):
            n = update[i]
            before_rules = {a for a, _ in filter(lambda rule: n == rule[1], rules)}
            after_rules = {b for _, b in filter(lambda rule: n == rule[0], rules)}

            for j in range(len(update)):
                m = update[j]

                violate_after = j < i and m in after_rules
                violate_before = j > i and m in before_rules
                if violate_before or violate_after:
                    return False

        return True

    middle_sum = 0
    for update in pages:
        if check_valid_order(update):
            middle = update[len(update) // 2]
            middle_sum += middle

    return middle_sum


def solve_part2(rules: list[tuple[int,int]], pages: list[list[int]]) -> int:
    def check_valid_order(update_in: list[int]) -> tuple[list[int], bool]:
        update = update_in.copy()
        any_modifications = False

        # Variation of bubble sort
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(update)):
                n = update[i]
                before_rules = {a for a, _ in filter(lambda rule: n == rule[1], rules)}
                after_rules = {b for _, b in filter(lambda rule: n == rule[0], rules)}

                for j in range(len(update)):
                    m = update[j]

                    violate_after = j < i and m in after_rules
                    violate_before = j > i and m in before_rules
                    if violate_before or violate_after:
                        any_modifications = True
                        
                        tmp = update[j]
                        update[j] = update[i]
                        update[i] = tmp
                        swapped = True

                        break

        return update, any_modifications

    middle_sum = 0
    for update in pages:
        update_sorted, changed = check_valid_order(update)
        if changed:
            middle = update_sorted[len(update) // 2]
            middle_sum += middle

    return middle_sum


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

rules, pages = parse_file(sys.argv[1])

sol1 = solve_part1(rules, pages)
print("part1:", sol1)

sol2 = solve_part2(rules, pages)
print("part2:", sol2)

