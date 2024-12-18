from __future__ import annotations
import sys
from copy import deepcopy
import time
import math
from typing import Callable

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"


def parse_file(filename: str) -> list[list[str]]:
    with open(filename) as fp:
        lines = fp.readlines()

    board = []
    for line in lines:
        board.append(list(line.strip()))

    return board


def clear_terminal():
    # print(chr(27) + "[2J")
    print("\n\n")


def print_board(board: list[list[str]], show_index: bool = False):
    rows = len(board)
    cols = len(board[0])
    pad_length = math.floor(math.log10(rows)) + 1

    header = ""
    if show_index:
        # Print index header
        for n in range(math.floor(math.log10(cols)), 0, -1):
            # Make digits for numbers above 10
            header += " " * pad_length + " "
            for c in range(cols):
                digit = c // (10 ** n)
                if digit == 0:
                    header += " "
                else:
                    header += str(digit)
            header += "\n"

            # Special case for digits below 10
            header += " " * pad_length + " "
            for c in range(cols):
                digit = c % 10
                header += str(digit)
            header += "\n"

    board_str = header
    for r in range(rows):
        if show_index:
            board_str += "{row:{width}} ".format(row=r, width=pad_length)

        for c in range(cols):
            board_str += board[r][c]
        board_str += "\n"
    
    if show_index:
        board_str += header

    print(board_str)


def print_path(board: list[list[str]], path: list[Node], show_index: bool = False):
    board_copy = deepcopy(board)
    for node in path:
        r, c = node.position
        board_copy[r][c] = "O"
    print_board(board_copy, show_index=show_index)


class Node:
    def __init__(self, position: tuple[int,int], state: str, came_from: Node | None):
        self.position = position
        self.state = state
        self.came_from = came_from
        self.cost_from_start = float("inf")  # g score
        self.best_guess_score = float("inf")  # f score

    def __repr__(self) -> str:
        return f"Node(state={self.state}, pos={self.position}, "\
               f"from={self.came_from.position if self.came_from else None}, "\
               f"g-score={self.cost_from_start}, f-score={self.best_guess_score}"



def taxicab_distance(pos: tuple[int,int] | Node, end: tuple[int,int]) -> int:
    # Taxicab distance
    if isinstance(pos, Node):
        return abs(end[0] - pos.position[0]) + abs(end[1] - pos.position[1])
    else:
        return abs(end[0] - pos[0]) + abs(end[1] - pos[1])


def distance_between_nodes(current: Node, neighbor: Node) -> int:
    state = current.state
    r1, c1 = current.position
    r2, c2 = neighbor.position

    is_east = c2 > c1
    is_west = c2 < c1
    is_north = r2 < r1
    is_south = r2 > r1

    # There are more conditions for when the score is 1000 than for when
    # it's 1, so set the default score to 1000 and set it to 1 in the rare
    # cases when that's true. 
    # Set the high score to 1001 (1000 + 1) because turning involves one
    # turn (cost of 1000) and one step forwards (cost of 1)
    score = 1001
    if state == RIGHT and is_east:
        score = 1
    elif state == LEFT and is_west:
        score = 1
    elif state == UP and is_north:
        score = 1
    elif state == DOWN and is_south:
        score = 1

    return score


def get_state(current: Node) -> str:
    if current.came_from is None:
        return current.state

    state = current.came_from.state
    r1, c1 = current.came_from.position
    r2, c2 = current.position

    is_east = c2 > c1
    is_west = c2 < c1
    is_north = r2 < r1
    is_south = r2 > r1

    new_state = state
    if state == RIGHT or state == LEFT:
        if is_north:
            new_state = UP
        elif is_south:
            new_state = DOWN
    elif state == UP or state == DOWN:
        if is_east:
            new_state = RIGHT
        elif is_west:
            new_state = LEFT
            
    return new_state


def a_star(start_: tuple[int,int], 
           end: tuple[int,int], 
           board: list[list[str]],
           heuristic_distance: Callable[[tuple[int,int]|Node,tuple[int,int]],int]) -> list[Node]:
    # Implementation of A* from:
    # https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
    rows = len(board)
    cols = len(board[0])

    grid: list[list[Node]] = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            grid[r].append(Node((r, c), board[r][c], None))

    r, c = start_
    start = grid[r][c]
    start.state = RIGHT
    start.cost_from_start = 0
    start.best_guess_score = heuristic_distance(start.position, end)

    horizon = [start]
    while len(horizon) > 0:
        # Sorting list to make it a priority queue
        horizon = sorted(horizon, key=lambda n: n.best_guess_score, reverse=True)
        current = horizon.pop()
        current.state = get_state(current)

        if current.position == end:
            # Finished, reconstruct the path
            path = []
            node = current
            while node.came_from is not None:
                path.append(node)
                node = node.came_from
            return path

        r, c = current.position
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            rr = r + dr
            cc = c + dc
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                continue

            neighbor = grid[rr][cc]

            if neighbor.state == WALL:
                continue

            move_cost = distance_between_nodes(current, neighbor)
            tentative_score = current.cost_from_start + move_cost
            neighbor_score = neighbor.cost_from_start

            if tentative_score < neighbor_score:
                neighbor.came_from = current
                neighbor.cost_from_start = tentative_score
                neighbor.best_guess_score = tentative_score + heuristic_distance(neighbor.position, end)

                if neighbor not in horizon:
                    horizon.append(neighbor)
    
    return []


def a_star_all(start_: tuple[int,int], end: tuple[int,int], board: list[list[str]]) -> list[list[Node]]:
    # Implementation of A* from:
    # https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
    rows = len(board)
    cols = len(board[0])

    grid: list[list[Node]] = []
    for r in range(rows):
        grid.append([])
        for c in range(cols):
            grid[r].append(Node((r, c), board[r][c], None))

    r, c = start_
    start = grid[r][c]
    start.state = RIGHT
    start.cost_from_start = 0
    start.best_guess_score = taxicab_distance(start.position, end)


    def reconstruct(current: Node) -> list[Node]:
        path = []
        node = deepcopy(current)
        while node.came_from is not None:
            path.append(deepcopy(node))
            node = node.came_from
        return path


    paths = []
    horizon = [deepcopy(start)]
    while len(horizon) > 0:
        # Sorting list to make it a priority queue
        horizon = sorted(horizon, key=lambda n: (n.best_guess_score, n.cost_from_start), reverse=True)
        current = horizon.pop()
        current.state = get_state(current)

        if current.position == end:
            # Finished, reconstruct the path
            path = reconstruct(current)
            paths.append(path)
            horizon.append(deepcopy(start))
            continue

        r, c = current.position
        for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            rr = r + dr
            cc = c + dc
            if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
                continue

            neighbor = grid[rr][cc]

            if neighbor.state == WALL:
                continue

            move_cost = distance_between_nodes(current, neighbor)
            tentative_score = current.cost_from_start + move_cost
            neighbor_score = neighbor.cost_from_start
            print("current", current.position, "neighbor", neighbor.position, "tentantive", tentative_score, "neighbor", neighbor_score)

            if tentative_score < neighbor_score:
                neighbor.came_from = current
                neighbor.cost_from_start = tentative_score
                neighbor.best_guess_score = tentative_score + taxicab_distance(neighbor.position, end)

                if neighbor not in horizon:
                    horizon.append(neighbor)


        horizon = sorted(horizon, key=lambda n: (n.best_guess_score, n.cost_from_start), reverse=True)
        clear_terminal()
        print("State:", current.state)
        print("Current:", current.position)
        print("Horizon:", list(map(lambda n: (*n.position, n.cost_from_start, n.best_guess_score), horizon)))
        print_path(board, reconstruct(current), True)
        if len(paths) > 0:
            input("Press Enter to go to next frame...")


    # Add an empty list if no path was found to symbolize no path
    if len(paths) == 0:
        paths.append([])

    return paths


def a_star_all2(start_: tuple[int,int], end: tuple[int,int], board: list[list[str]]) -> list[list[Node]]:
    
    def heuristic(pos: tuple[int,int] | Node, end: tuple[int,int]) -> int:
        taxi = taxicab_distance(pos, end)
        for path in paths:
            for node in path:
                if pos == node.position:
                    taxi += 500
        return taxi

    paths = []
    count = 0
    while count < 2: # True:
        path = a_star(start_, end, board, heuristic)
        if path in paths:
            break
        paths.append(path)
        count += 1

    if len(paths) == 0:
        paths.append([])

    return paths


def solve_part1(board: list[list[str]]) -> int:
    rows = len(board)
    cols = len(board[0])

    # Find start and end
    start = (-1, -1)
    end = (-1, -1)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == START:
                start = (r, c)
            elif board[r][c] == END:
                end = (r, c)

    shortest_path = a_star(start, end, board, taxicab_distance)

    return int(shortest_path[0].cost_from_start)


def solve_part2(board: list[list[str]]) -> int:
    rows = len(board)
    cols = len(board[0])

    # Find start and end
    start = (-1, -1)
    end = (-1, -1)
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == START:
                start = (r, c)
            elif board[r][c] == END:
                end = (r, c)

    print("Board")
    print_board(board)
    print()

    # IDEA: Instead of having Node.came_from as a single Node, have a list
    # of nodes
    shortest_paths = a_star_all2(start, end, board)

    total_cost = 0
    for i, path in enumerate(shortest_paths):
        print(f"\nPath #{i}")
        print_path(board, path)

    return total_cost


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

board = parse_file(sys.argv[1])

sol1 = solve_part1(deepcopy(board))
print("part1:", sol1)

sol2 = solve_part2(deepcopy(board))
print("part2:", sol2)

