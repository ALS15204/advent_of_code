from functools import cache
from collections import Counter

SPLIT_CACHES = {}


@cache
def split_number(number_str: str):
    if number_str in SPLIT_CACHES:
        return SPLIT_CACHES[number_str]
    if number_str == "0":
        SPLIT_CACHES[number_str] = "1"
    elif len(number_str) % 2 == 0:
        division = len(number_str) // 2
        SPLIT_CACHES[number_str] = f"{number_str[:division]} {int(number_str[division:])}"
    else:
        SPLIT_CACHES[number_str] = f"{int(number_str) * 2024}"
    return SPLIT_CACHES[number_str]


def break_numbers(number_str: str):
    yield from number_str.strip().split()


def blink(initial_numbers, steps):
    num_count = Counter(iter(break_numbers(initial_numbers)))
    all_numbers = set(num_count)
    for _ in range(steps):
        final_count = Counter()
        for num in all_numbers:
            new_numbers = split_number(num).split()
            count = num_count.pop(num)
            for new_num in new_numbers:
                final_count[new_num] += count
        all_numbers = set(final_count)
        num_count = final_count
    return final_count if steps > 0 else num_count


if __name__ == "__main__":
    with open("data/input.dat") as f:
        number_strs = f.read().strip()

    print(sum(blink(number_strs, 25).values()))
    print(sum(blink(number_strs, 75).values()))
