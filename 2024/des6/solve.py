import sys
from copy import deepcopy

def parse_file(filename: str) -> list[list[str]]:
    with open(filename) as fp:
        board = [ 
            list(line.strip()) for line in fp.readlines()
        ]

    return board


def print_board(board: list[list[str]]):
    for row in board:
        print("".join(row))


def solve_part1(board_original: list[list[str]]) -> int:
    board = deepcopy(board_original)
    rows = len(board)
    cols = len(board[0])
    possible_directions = ["^", ">", "v", "<"]

    def walk(start: tuple[int,int]) -> tuple[tuple[int,int], list[tuple[int,int]], bool]:
        """
        Walk until an obstruction #.
        Return:
            new position
            path
            still within the board
        """
        r, c = start
        guard = board[r][c]

        # Direction is specified as (direction_rows, direction_cols) where
        # each element would be added to the current position to walk one cell
        direction = (None, None)
        if guard == "^":
            direction = (-1, 0)
        elif guard == ">":
            direction = (0, 1)
        elif guard == "v":
            direction = (1, 0)
        elif guard == "<":
            direction = (0, -1)
        else:
            raise ValueError(f"Guard direction '{guard}' is invalid")

        def within(row: int, col: int) -> bool:
            return 0 <= row < rows and 0 <= col < cols

        move_path = []
        still_within = False
        while (still_within := within(r, c)) and board[r][c] != "#":
            r += direction[0]
            c += direction[1]
            move_path.append((r, c))

        # Substract once because r,c will be ON the # cell when the loop exits
        r -= direction[0]
        c -= direction[1]
        move_path.pop()

        return (r, c), move_path, still_within

    # find initial position
    guard_pos = (-1, -1)  # (row, col)
    guard_direction = -1  # index into possible_positions
    for r in range(rows):
        for c in range(cols):
            if board[r][c] in possible_directions:
                guard_pos = (r, c)
                guard_direction = possible_directions.index(board[r][c])
                break

    unique_cells = set()
    still_within = True
    while still_within:
        new_guard_pos, move_path, still_within = walk(guard_pos)
        unique_cells.update(move_path)

        # Set old position
        r, c = guard_pos
        board[r][c] = "."

        guard_direction = (guard_direction + 1) % len(possible_directions)
        r, c = new_guard_pos
        board[r][c] = possible_directions[guard_direction]
        guard_pos = new_guard_pos

    return len(unique_cells)


def solve_part2(board_original: list[list[str]]) -> int:
    pass


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])
print_board(puzzle_input)

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

