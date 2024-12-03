import re

MUL_REGEX = re.compile(r"mul\((\d+),(\d+)\)")
DONTS = re.compile(r"don't\(\)")
DOS = re.compile(r"do\(\)")


if __name__ == "__main__":
    with open("data/input.dat") as f:
        lines = [line.strip() for line in f.readlines()]

    total_sum = 0
    for line in lines:
        mul_groups = MUL_REGEX.findall(line)
        total_sum += sum(int(a) * int(b) for a, b in mul_groups)

    print(total_sum)

    total_sum = 0
    off = False
    for line in lines:
        donts = list(DONTS.finditer(line))
        donts = [m.regs[0][-1] for m in donts]
        dos = list(DOS.finditer(line))
        dos = [m.regs[0][-1] for m in dos]
        flags = [int(not off) for _ in range(len(line))]
        for idx, _ in enumerate(flags):
            if idx in donts:
                off = True
            if idx in dos:
                off = False
            flags[idx] = int(not off)
        for mul_match in MUL_REGEX.finditer(line):
            start, end = mul_match.regs[0]
            a, b = mul_match.groups()
            total_sum += int(a) * int(b) * flags[start]
    print(total_sum)