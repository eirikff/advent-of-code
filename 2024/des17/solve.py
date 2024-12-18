import sys
import time

def parse_file(filename: str) -> tuple[dict[str,int],list[int]]:
    with open(filename) as fp:
        lines = fp.readlines()

    def parse_register(line: str) -> tuple[str,int]:
        reg, val = line.split(": ")
        reg = reg[-1]
        val = int(val)
        return reg, val

    regs = {
        reg: val for reg, val in [parse_register(line) for line in lines[:3]]
    }
    
    program_line = lines[-1].split(" ")[1]
    program = [int(d) for d in program_line.split(",")]

    return regs, program


class Computer:
    def __init__(self, program: list[int], A: int = 0, B: int = 0, C: int = 0):
        self.program = program
        self.regA = A
        self.regB = B
        self.regC = C

        self.debug = False
        self.trace = False
        self.ip = 0
        self.output: list[int] = []
        self.opcode = {
            0: self.adv,  # A = A / 2^combo = A >> combo
            1: self.bxl,  # B = B ^ op
            2: self.bst,  # B = combo % 8 = combo & 7
            3: self.jnz,  # ip = op OR nop (A = 0)
            4: self.bxc,  # B = B ^ C
            5: self.out,  # print combo % 8 = combo & 7
            6: self.bdv,  # B = A / 2^combo = A >> combo
            7: self.cdv,  # C = A / 2^combo = A >> combo
        }

    def __repr__(self) -> str:
        return f"Computer(A={self.regA}, B={self.regB}, C={self.regC}, ip={self.ip}, dbg={self.debug}, pgrm={self.program})"

    def execute(self, max_cycles: int = -1) -> list[int]:
        self.ip = 0
        cycles = 0
        while self.ip < len(self.program):
            inst = self.program[self.ip]
            op = self.program[self.ip + 1]
            self.opcode[inst](op)
            if self.trace: self.print_trace()

            cycles += 1
            if max_cycles > 0 and cycles == max_cycles:
                print(f"[warn] Program did not finish after {cycles} cycles")
                break

        if self.debug:
            print(f"Program exit after {cycles} cycles, output:", ",".join(str(d) for d in self.output))

        return self.output

    def toggle_debug(self):
        self.debug = not self.debug

    def toggle_trace(self):
        self.trace = not self.trace

    def increment_ip(self):
        self.ip += 2
        if self.debug: print(f"[incr ip] ip incremented to {self.ip}")

    def print_trace(self):
        print(f"[trace]")
        print(f"    ip = {self.ip}")
        print(f"    A = {self.regA}")
        print(f"    B = {self.regB}")
        print(f"    C = {self.regC}")
        print(f"    output = {self.output}")

    def combo(self, operand: int) -> int:
        if 0 <= operand <= 3:
            if self.debug: print(f"[combo] in {operand} is literal {operand}")
            return operand
        elif operand == 4:
            if self.debug: print(f"[combo] in {operand} is A {self.regA}")
            return self.regA
        elif operand == 5:
            if self.debug: print(f"[combo] in {operand} is B {self.regB}")
            return self.regB
        elif operand == 6:
            if self.debug: print(f"[combo] in {operand} is C {self.regC}")
            return self.regC
        else:
            raise ValueError(f"Combo operand {operand} is invalid.")


    def adv(self, operand: int):
        assert operand.bit_length() <= 3

        combo = self.combo(operand)
        numerator = self.regA
        denominator = 2 ** combo
        self.regA = numerator // denominator

        if self.debug: 
            print(f"[adv,0] op {operand} = combo {combo}, A = {numerator} / {denominator} = {self.regA}")

        self.increment_ip()

    def bxl(self, operand: int):
        assert operand.bit_length() <= 3

        newB = self.regB ^ operand
        if self.debug:
            print(f"[bxl,1] op {operand}, B = {self.regB} ^ {operand} = {newB}")

        self.regB = newB
        self.increment_ip()

    def bst(self, operand: int):
        assert operand.bit_length() <= 3

        combo = self.combo(operand)
        newB = combo % 8
        if self.debug:
            print(f"[bst,2] op {operand} = combo {combo}, B = {combo} % 8 = {newB}")

        self.regB = newB
        self.increment_ip()

    def jnz(self, operand: int):
        assert operand.bit_length() <= 3

        if self.regA == 0:
            if self.debug:
                print(f"[jnz,3] op {operand}, A = 0, do nothing")
            self.increment_ip()  # TODO: correct to increment here?
            return

        if self.debug:
            print(f"[jnz,3] op {operand}, A = {self.regA}, old ip = {self.ip}, new ip = {operand}")

        self.ip = operand

    def bxc(self, operand: int):
        assert operand.bit_length() <= 3

        newB = self.regC ^ self.regB
        if self.debug:
            print(f"[bxc,4] op {operand} (ignored), B = B ^ C = {self.regB} ^ {self.regC} = {newB}")

        self.regB = newB
        self.increment_ip()

    def out(self, operand: int):
        assert operand.bit_length() <= 3
        
        combo = self.combo(operand)
        out = combo % 8
        self.output.append(out)

        if self.debug:
            print(f"[out,5] op {operand} = combo {combo}, out = {combo} % 8 = {out}, output {self.output}")

        self.increment_ip()

    def bdv(self, operand: int):
        assert operand.bit_length() <= 3

        combo = self.combo(operand)
        numerator = self.regA
        denominator = 2 ** combo
        self.regB = numerator // denominator

        if self.debug: 
            print(f"[bdv,6] op {operand} = combo {combo}, B = {numerator} / {denominator} = {self.regB}")

        self.increment_ip()

    def cdv(self, operand: int):
        assert operand.bit_length() <= 3

        combo = self.combo(operand)
        numerator = self.regA
        denominator = 2 ** combo
        self.regC = numerator // denominator

        if self.debug: 
            print(f"[cdv,7] op {operand} = combo {combo}, C = {numerator} / {denominator} = {self.regC}")

        self.increment_ip()

    def pprint(self):
        opcode_str = {
            0: "adv",
            1: "bxl",
            2: "bst",
            3: "jnz",
            4: "bxc",
            5: "out",
            6: "bdv",
            7: "cdv",
        }
        combo_str = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: "A",
            5: "B",
            6: "C",
            7: "invalid",
        }

        print("Computer:")
        print(f"\tA = {self.regA}")
        print(f"\tB = {self.regB}")
        print(f"\tC = {self.regC}")
        print(f"\tprogram length = {len(self.program)}")
        print(f"\tdebug = {self.debug}")
        print(f"\ttrace = {self.trace}")
        print("\nProgram listing:")
        for ip in range(0, len(self.program) - 1, 2):
            inst = self.program[ip]
            op = self.program[ip+1]

            print(f"\t{opcode_str[inst]} {op}\t(combo: {combo_str[op]})")


def solve_part1(registers: dict[str,int], program: list[int]) -> str:
    comp = Computer(program, **registers)
    # comp.pprint()
    # comp.toggle_debug()
    # comp.toggle_trace()
    result = comp.execute()

    return ",".join(str(d) for d in result)


def solve_part2(registers: dict[str,int], program: list[int]) -> int:
    comp = Computer(program, 0, 0, 0)

    # Initial A must be in range 2**45 to 2**48
    # 2**45 = 1 << 3*15  (gives output length 16, 2**45 - 1 gives length 15)
    # 2**48 = 1 << 3*16  (gives output length 17, 2**48 - 1 gives length 16)
    initial_a = 0
    for i in reversed(range(len(program))):
        for b in range(8):
            comp.regA = initial_a | b
            comp.regB = 0
            comp.regC = 0
            comp.output = []
            output = comp.execute(10000)
            print(b, output)
            if output[0] == program[i]:
                break

        initial_a = b << (3*i) | initial_a
        print(i, initial_a, bin(initial_a))

    print(initial_a)
    output = Computer(program, A=initial_a).execute(10000)
    print(output)
    print("program", program)
    return initial_a


if len(sys.argv) != 2:
    print(f"{sys.argv[0]} [input file]")
    exit(1)

registers, program = parse_file(sys.argv[1])

sol1 = solve_part1(registers, program)
print("part1:", sol1)

t0 = time.time()
sol2 = solve_part2(registers, program)
t1 = time.time()
print("part2:", sol2, f"(finished in {t1 - t0:.2f}s)")

