from collections import Counter


if __name__ == "__main__":
    first_numbers = []
    second_numbers = []
    with open("input.dat") as f:
        for line in f:
            num_1, num_2 = [int(x) for x in line.strip().split()]
            first_numbers.append(num_1)
            second_numbers.append(num_2)

    distances = [abs(num_1 - num_2) for num_1, num_2 in zip(sorted(first_numbers), sorted(second_numbers))]
    print(sum(distances))

    count_second_numbers = Counter(second_numbers)
    similarity = sum(
        num * count_second_numbers.get(num, 0) for num in first_numbers
    )
    print(similarity)