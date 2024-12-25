import sys
import time
from pprint import pprint


MODULUS = 16777216


def parse_file(filename: str) -> list[int]:
    with open(filename) as fp:
        lines = fp.readlines()

    numbers = [int(d.strip()) for d in lines]
    return numbers


def mix(secret: int, mixin: int) -> int:
    return secret ^ mixin


def prune(secret: int) -> int:
    return secret % MODULUS


def mix_then_prune(secret: int, mixin: int) -> int:
    return prune(mix(secret, mixin))


def evolve_once(secret: int) -> int:
    m = secret * 64
    secret = mix_then_prune(secret, m)

    m = secret // 32
    secret = mix_then_prune(secret, m)
    
    m = secret * 2048
    secret = mix_then_prune(secret, m)

    return secret


def solve_part1(numbers: list[int]) -> int:
    secrets = []
    for n in numbers:
        secret = n
        for _ in range(2000):
            secret = evolve_once(secret)
        secrets.append(secret)

    return sum(secrets)


def solve_part2(numbers: list[int]) -> int:
    all_quadruplets = []
    for initial_secret in numbers:
        secret = initial_secret

        secrets = [secret]
        prices = [secret % 10]
        deltas = [0]
        quadruplets = {}
        
        old_price = prices[0]
        for i in range(2000):
            secret = evolve_once(secret)
            secrets.append(secret)

            price = secret % 10
            prices.append(price)

            delta = price - old_price
            deltas.append(delta)
            old_price = price

            if i >= 4:
                last_four = tuple(deltas[-4:])

                # Store the price only the first time a quadruplet occurs
                if last_four not in quadruplets:
                    quadruplets[last_four] = price

        all_quadruplets.append(quadruplets)

    sums = {}
    for quadruplets in all_quadruplets:
        for last_four, price in quadruplets.items():
            sums[last_four] = sums.get(last_four, 0) + price

    max_sum = max(sums.values())
    return max_sum


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

numbers = parse_file(sys.argv[1])

t0 = time.time()
sol1 = solve_part1(numbers)
t1 = time.time()
print("part1:", sol1, f"(elapsed time: {t1 - t0:.3f}s)")

t0 = time.time()
sol2 = solve_part2(numbers)
t1 = time.time()
print("part2:", sol2, f"(elapsed time: {t1 - t0:.3f}s)")

