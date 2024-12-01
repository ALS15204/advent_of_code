from pathlib import Path

from day3.utils import RuckSack, letter_to_priority


SCRIPT_DIR = Path(__file__).parent
LINE_BREAK = "\n"
NUM_PER_GROUP = 3


if __name__ == "__main__":
    with open(SCRIPT_DIR / "input.dat", "r") as input_file:
        lines = input_file.readlines()

    lines = [line.replace(LINE_BREAK, "") for line in lines if line]
    rucksacks = [RuckSack(line) for line in lines]
    assert all(rucksack.num_items_is_even for rucksack in rucksacks)
    assert all(rucksack.only_one_type_misplaced for rucksack in rucksacks)

    print(
        f"Part One: sum of priority of misplaced item types is "
        f"{sum(sum(rucksack.misplaced_items_priority) for rucksack in rucksacks)}"
    )

    all_badges = []
    for i_group in range(len(rucksacks) // NUM_PER_GROUP):
        idx_start = i_group * NUM_PER_GROUP
        group_members = rucksacks[idx_start: idx_start + NUM_PER_GROUP]
        matching_items = set()
        for member in group_members[1:]:
            if not matching_items:
                matching_items |= group_members[0].matching_items(member)
            else:
                matching_items = matching_items.intersection(group_members[0].matching_items(member))
        assert len(matching_items) == 1
        all_badges.append(letter_to_priority(matching_items.pop()))
    print(f"Part Two: sum of badge priorities is {sum(all_badges)}.")