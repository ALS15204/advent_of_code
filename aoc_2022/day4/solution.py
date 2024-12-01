from pathlib import Path

from day4.utils import CleanRange

SCRIPT_DIR = Path(__file__).parent
LINE_BREAK = "\n"

if __name__ == "__main__":
    with open(SCRIPT_DIR / "input.dat", "r") as input_file:
        lines = input_file.readlines()

    range_tuples = [
        ([CleanRange(x.strip()) for x in line.split(",")]) for line in lines if line
    ]
    fully_covered = [(range_1.contains(range_2) or range_1.is_subset(range_2)) for range_1, range_2 in range_tuples]

    print(f"Part One: there are {sum(fully_covered)} fully overlapped groups.")

    overlaps = [range_1.overlap(range_2) for range_1, range_2 in range_tuples]
    print(f"Part Two: there are {sum(len(o) > 0 for o in overlaps)} overlapping ranges.")