import sys


class Game:
    class Button:
        def __init__(self, x: int, y: int):
            self.x = x 
            self.y = y

        def __repr__(self) -> str:
            return f"(x={self.x}, y={self.y})"

    def __init__(self, A: tuple[int,int], B: tuple[int,int], prize: tuple[int,int]):
        self.A = Game.Button(*A)
        self.B = Game.Button(*B)
        self.prize = Game.Button(*prize)

    def __repr__(self) -> str:
        return f"Game(A={self.A}, B={self.B}, prize={self.prize})"

    def matrix_solve(self) -> tuple[int,int] | None:
        # Define inverse of 2x2 matrix
        # [ Ax Bx ] = 1/det [  By -Bx ]
        # [ Ay By ]         [ -Ay  Ax ]
        # Determinant is the same
        m11 = self.B.y
        m22 = self.A.x
        m12 = -self.B.x
        m21 = -self.A.y
        det = m11 * m22 - m12 * m21

        # Prize vector
        p1 = self.prize.x
        p2 = self.prize.y

        a = m11 * p1 + m12 * p2
        b = m21 * p1 + m22 * p2
        
        if a % det == 0 and b % det == 0:
            return (a // det, b // det)
        else:
            return None


def parse_file(filename: str) -> list[Game]:
    with open(filename) as fp:
        chunks = fp.read().split("\n\n")

    def parse_line(btn_line: str) -> tuple[int,int]:
        _, coords = btn_line.split(": ")
        x, y = coords.split(", ")
        x = int(x[2:])
        y = int(y[2:])
        return x, y

    games = []
    for chunk in chunks:
        btnA_line, btnB_line, prize_line = chunk.strip().split("\n")
        a = parse_line(btnA_line)
        b = parse_line(btnB_line)
        p = parse_line(prize_line)

        games.append(Game(a, b, p))

    return games


def solve_part1(games: list[Game]) -> int:
    token_cost_A = 3
    token_cost_B = 1

    total_cost = 0
    for game in games:
        if sol := game.matrix_solve():
            total_cost += sol[0] * token_cost_A + sol[1] * token_cost_B

    return total_cost


def solve_part2(games: list[Game]) -> int:
    token_cost_A = 3
    token_cost_B = 1

    total_cost = 0
    for game in games:
        # Modifications for part 2
        game.prize.x += 10000000000000
        game.prize.y += 10000000000000

        if sol := game.matrix_solve():
            total_cost += sol[0] * token_cost_A + sol[1] * token_cost_B

    return total_cost


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

puzzle_input = parse_file(sys.argv[1])

sol1 = solve_part1(puzzle_input)
print("part1:", sol1)

sol2 = solve_part2(puzzle_input)
print("part2:", sol2)

