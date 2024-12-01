from pathlib import Path


SCRIPT_DIR = Path(__file__)
INPUT_FILE = SCRIPT_DIR.parent / "input.dat"
ELF_SEPARATOR = "\n\n"
ITEM_SEPARATOR = "\n"

if __name__ == "__main__":
    with open(INPUT_FILE, "r") as input_file:
        lines = input_file.readlines()

    lines = "".join(lines)
    lines = [x.split(ITEM_SEPARATOR) for x in lines.split(ELF_SEPARATOR)]
    lines = [list(map(int, line.pop(-1) if "" in line else line)) for line in lines]

    max_idx, max_items = max(enumerate(lines), key=lambda x: sum(x[1]))
    print(f"Part One: The {max_idx + 1}th is carrying the most calories of {sum(max_items)} calories.")

    top_3_idx_items_tuples = sorted(enumerate(lines), key=lambda x: sum(x[1]))[::-1][:3]
    print(f"Part Two: The {[x[0] + 1 for x in top_3_idx_items_tuples]} are carrying the most calories of "
          f"{sum(sum(x[1]) for x in top_3_idx_items_tuples)} calories.")
