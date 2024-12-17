class Computer:
    def __init__(self, A: int, B: int, C: int):
        self.A = A
        self.B = B
        self.C = C
        self.opo_code_to_function = {
            0: self.opo_0,
            1: self.opo_1,
            2: self.opo_2,
            3: self.opo_3,
            4: self.opo_4,
            5: self.opo_5,
            6: self.opo_6,
            7: self.opo_7,
        }

    def _combo(self, value: int) -> int:
        if 0 <= value <= 3:
            return value
        if value == 4:
            return self.A
        if value == 5:
            return self.B
        if value == 6:
            return self.C

    def opo_0(self, instruction: int):
        self.A = int(self.A / 2 ** (self._combo(instruction)))

    def opo_1(self, instruction: int):
        self.B = self.B ^ instruction

    def opo_2(self, instruction: int):
        self.B = self._combo(instruction) % 8

    def opo_3(self, instruction: int):
        if self.A != 0:
            return instruction

    def opo_4(self, instruction: int):
        self.B = self.B ^ self.C

    def opo_5(self, instruction: int):
        return f"{self._combo(instruction) % 8}"

    def opo_6(self, instruction: int):
        self.B = int(self.A / 2 ** (self._combo(instruction)))

    def opo_7(self, instruction: int):
        self.C = int(self.A / 2 ** (self._combo(instruction)))

    def run(self, programs: str):
        programs = iter(programs.split(","))
        programs = [(int(x), int(y)) for x, y in zip(programs, programs)]
        n_instruction = 0
        result = ""
        while n_instruction < len(programs):
            opo_code, instruction = programs[n_instruction]
            output = self.opo_code_to_function[opo_code](instruction)
            if isinstance(output, int):
                n_instruction = output
                continue
            elif isinstance(output, str):
                result += f",{output}"
            n_instruction += 1
        return result.strip(",")


if __name__ == "__main__":
    with open("data/input.dat") as file:
        registers, programs = file.read().split("\n\n")
        A, B, C = [int(x.split()[-1]) for x in registers.split("\n")]
        programs = programs.split()[-1]
    computer = Computer(A, B, C)
    print(computer.run(programs))

    A = sum(7 * 8**i for i in range(len(programs.split(",")) - 1)) + 1
    output = ""
    while output != programs:
        computer = Computer(A, B, C)
        output = computer.run(programs)
        add = 0
        for i in range(len(output.split(",")) - 1, -1, -1):
            if output.split(",")[i] != programs.split(",")[i]:
                add = 8 ** i
                A += add
                break
    print(A)
