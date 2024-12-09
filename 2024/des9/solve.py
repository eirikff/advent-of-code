import sys
import itertools
import time

FREE_SPACE_ID = None

def parse_file(filename: str) -> list[int]:
    with open(filename) as fp:
        disk_map = [int(d) for d in fp.read().strip()]
    
    # Expand disk map to memory map
    memory_map = []
    id_counter = itertools.count()
    for i, n in enumerate(disk_map):
        is_block = i % 2 == 0
        if is_block:
            block_id = next(id_counter)
            size = n
        else:
            block_id = FREE_SPACE_ID
            size = n

        memory_map += [block_id] * size

    return memory_map


def checksum(memory_map: list[int]) -> int:
    cc = 0
    for i in range(len(memory_map)):
        if memory_map[i] == FREE_SPACE_ID:
            continue
        cc += i * memory_map[i]
    return cc


def solve_part1(memory_map: list[int]) -> int:
    rearranged = memory_map.copy()

    # Rearrange blocks to beginning of memory map
    def find_backward(idx: int) -> int:
        assert 0 <= idx < len(rearranged), "Index out of range"
        while rearranged[idx] is FREE_SPACE_ID:
            idx -= 1
        return idx

    def find_forward(idx: int) -> int:
        assert 0 <= idx < len(rearranged), "Index out of range"
        while rearranged[idx] is not FREE_SPACE_ID:
            idx += 1
        return idx

    take_index = find_backward(len(rearranged) - 1)
    place_index = find_forward(0)

    while place_index < take_index:
        rearranged[place_index] = rearranged[take_index]
        rearranged[take_index] = FREE_SPACE_ID  # pyright: ignore

        take_index = find_backward(take_index)
        place_index = find_forward(place_index)

    return checksum(rearranged)


def solve_part2(memory_map: list[int]) -> int:
    rearranged = memory_map.copy()

    def find_block(id: int = -1, *, start: int = len(rearranged) - 1) -> tuple[int,int,int]:
        """
        Finds the start and size of block with id. If id is -1, finds the last
        block of any id.
        """
        if id == -1:
            idx = start
            while rearranged[idx] == FREE_SPACE_ID:
                idx -= 1
            id = rearranged[idx]

        block_end = start
        while rearranged[block_end] != id:
            block_end -= 1

        block_start = block_end
        while block_start >= 0 and rearranged[block_start] == id:
            block_start -= 1

        block_size = block_end - block_start
        # Add 1 because the last while loop ends on the number before the block
        # starts
        block_start += 1
        return block_start, block_size, id

    def find_free(*, start: int = 0) -> tuple[int,int]:
        free_start = start
        while rearranged[free_start] != FREE_SPACE_ID:
            free_start += 1

        free_end = free_start
        while free_end < len(rearranged) and rearranged[free_end] == FREE_SPACE_ID:
            free_end += 1

        free_size = free_end - free_start
        return free_start, free_size

    block_start, block_size, block_id = find_block()
    free_start, free_size = find_free()

    while block_start >= 0:
        # Look for big enough free space
        free_start, free_size = find_free()
        while free_size < block_size and free_start < block_start:
            free_start, free_size = find_free(start=free_start + free_size)

        if free_start >= block_start:
            # No free space large enough exists
            block_start, block_size, block_id = find_block(start=block_start - 1)
            continue

        if block_size <= free_size:
            for i in range(block_size):
                rearranged[free_start + i] = block_id
                rearranged[block_start + i] = FREE_SPACE_ID  # pyright: ignore

            block_start, block_size, block_id = find_block(start=block_start - 1)
            free_start, free_size = find_free()

    return checksum(rearranged)


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

t0 = time.time()
sol1 = solve_part1(puzzle_input)
t1 = time.time()
print("part1:", sol1, f"(time elpased {t1 - t0:.4f}s)")

t0 = time.time()
sol2 = solve_part2(puzzle_input)
t1 = time.time()
print("part2:", sol2, f"(time elpased {t1 - t0:.4f}s)")

