from typing import List
from itertools import combinations


def is_monotonic(numbers: List[int]) -> bool:
    if all(numbers[i] < numbers[i + 1] for i in range(len(numbers) - 1)):
        return True
    return all((numbers[i] > numbers[i + 1] for i in range(len(numbers) - 1)))


def change_by_threshold(numbers: List[int], threshold: int = 3) -> bool:
    return all(1 <= abs(numbers[i] - numbers[i + 1]) <= threshold for i in range(len(numbers) - 1))


if __name__ == "__main__":
    with open("data/input.dat") as f:
        red_nosed_reports = [[int(x) for x in line.strip().split()] for line in f]

    # Part 1:
    safe_or_not = [is_monotonic(report) and change_by_threshold(report) for report in red_nosed_reports]
    n_safe = sum(safe_or_not)
    print(n_safe)

    # Part 2:
    for is_safe, report in zip(safe_or_not, red_nosed_reports):
        if not is_safe:
            for comb in combinations(report, len(report) - 1):
                if is_monotonic(comb) and change_by_threshold(comb):
                    n_safe += 1
                    break
    print(n_safe)
