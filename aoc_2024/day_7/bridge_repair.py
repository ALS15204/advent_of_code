import itertools

PLUS = "+"
MULTIPLY = "*"
COMBINE = "|"
SPACE = " "
OPERATORS = {PLUS: lambda x, y: x + y, MULTIPLY: lambda x, y: x * y}
NEW_OPERATORS = {PLUS: lambda x, y: x + y, MULTIPLY: lambda x, y: x * y, COMBINE: lambda x, y: int(f"{x}{y}")}


if __name__ == "__main__":
    with open("data/input.dat") as f:
        data_lines = f.read().splitlines()

    calibration = 0
    new_calibration = 0
    for line in data_lines:
        result = None
        test_value, all_numbers_str = line.split(":")
        test_value = int(test_value)
        all_numbers_str = all_numbers_str.strip()
        all_numbers = [int(x) for x in all_numbers_str.split()]
        possible_operations = set(itertools.product(OPERATORS, repeat=len(all_numbers) - 1))
        for operation in possible_operations:
            result = all_numbers[0]
            for i_op, op in enumerate(operation):
                result = OPERATORS[op](result, all_numbers[i_op + 1])
            if result == test_value:
                calibration += result
                break
        if result and result != test_value:
            possible_operations = set(itertools.product(NEW_OPERATORS, repeat=len(all_numbers) - 1))
            possible_operations = {op for op in possible_operations if COMBINE in op}
            for operation in possible_operations:
                result = all_numbers[0]
                for i_op, op in enumerate(operation):
                    result = NEW_OPERATORS[op](result, all_numbers[i_op + 1])
                if result == test_value:
                    new_calibration += result
                    break
    print(calibration)
    print(calibration + new_calibration)