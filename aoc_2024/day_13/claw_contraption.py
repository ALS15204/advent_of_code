import re

STEP_RE = re.compile(r"X\+(\d+), Y\+(\d+)")
POSITION_RE = re.compile(r"X=(\d+), Y=(\d+)")
COST_A = 3
COST_B = 1
OFFSET = 10000000000000


def solve_a_b(step_a, step_b, final_position, tolerance=1e-6):
    a = ((final_position[1] - final_position[0] * step_b[1] / step_b[0]) /
         (step_a[1] - step_a[0] * step_b[1] / step_b[0]))
    b = (final_position[0] - a * step_a[0]) / step_b[0]
    return (
        None
        if abs(round(a) - a) >= tolerance
        or abs(round(b) - b) >= tolerance
        else (round(a), round(b))
    )


if __name__ == '__main__':
    with open("data/input.dat", "r") as f:
        games = f.read().split("\n\n")

    total_cost = 0
    for game in games:
        step_a_str, step_b_str, final_position_str = game.strip().split("\n")
        step_a = tuple(map(int, STEP_RE.search(step_a_str).groups()))
        step_b = tuple(map(int, STEP_RE.search(step_b_str).groups()))
        final_position = tuple(map(int, POSITION_RE.search(final_position_str).groups()))
        if result := solve_a_b(step_a, step_b, final_position):
            if all(0 < i <= 100 for i in result):
                total_cost += COST_A * result[0] + COST_B * result[1]
    print(total_cost)

    total_cost = 0
    for game in games:
        step_a_str, step_b_str, final_position_str = game.strip().split("\n")
        step_a = tuple(map(int, STEP_RE.search(step_a_str).groups()))
        step_b = tuple(map(int, STEP_RE.search(step_b_str).groups()))
        final_position = tuple(map(int, POSITION_RE.search(final_position_str).groups()))
        final_position = (final_position[0] + OFFSET, final_position[1] + OFFSET)
        if result := solve_a_b(step_a, step_b, final_position, tolerance=1E-3):
            if all(i >= 0 for i in result):
                total_cost += COST_A * result[0] + COST_B * result[1]
    print(total_cost)