from typing import List

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
UPPER_LEFT = (-1, -1)
UPPER_RIGHT = (1, -1)
LOWER_LEFT = (-1, 1)
LOWER_RIGHT = (1, 1)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UPPER_LEFT, UPPER_RIGHT, LOWER_LEFT, LOWER_RIGHT]
MAS = ["M", "A", "S"]
MS = ["M", "S"]


def get_neighbors(
        grid: List[List[str]], row: int, col: int, step: int = 3, directions: List[tuple] = None
) -> List[List[str]]:
    if directions is None:
        directions = DIRECTIONS
    neighbors = []
    for direction in directions:
        neighbor = []
        for s in range(1, step + 1):
            r = row + direction[1] * s
            c = col + direction[0] * s
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                neighbor.append(grid[r][c])
        if len(neighbor) == step:
            neighbors.append(neighbor)
    return neighbors


def concatenate_lists(lists: List[List[str]]) -> List[str]:
    result = []
    for lst in lists:
        result.extend(lst)
    return result


if __name__ == "__main__":

    with open("data/input.dat", "r") as f:
        grid = [list(line.strip()) for line in f.readlines()]

    count = 0
    for row, grid_line in enumerate(grid):
        for col, char in enumerate(grid_line):
            if char == "X":
                count += get_neighbors(grid, row, col).count(MAS)
    print(count)

    count = 0
    for row, grid_line in enumerate(grid):
        for col, char in enumerate(grid_line):
            if char == "A":
                left_top_down = set(
                    concatenate_lists(get_neighbors(grid, row, col, step=1, directions=[UPPER_LEFT, LOWER_RIGHT]))
                )
                right_top_down = set(
                    concatenate_lists(get_neighbors(grid, row, col, step=1, directions=[UPPER_RIGHT, LOWER_LEFT]))
                )
                if left_top_down == right_top_down == set(MS):
                    count += 1
    print(count)
