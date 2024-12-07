DIRECTIONS = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
TURN_SEQUENCE = {"^": ">", ">": "v", "v": "<", "<": "^"}


class Map:

    MAP_CHARS = {"#", "."}

    def __init__(self, map_data):
        self.map = {(x, y): map_data[y][x] for y in range(len(map_data)) for x in range(len(map_data[0]))}
        self.width = len(map_data[0])
        self.height = len(map_data)
        self.visited = {(x, y): False for y in range(self.height) for x in range(self.width)}
        (guard_x, guard_y), _ = self.find_guard()
        self.visited[(guard_x, guard_y)] = True

    def get(self, x, y):
        return self.map.get((x, y), None)

    def is_wall(self, x, y):
        return self.get(x, y) == '#'

    def find_guard(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.get(x, y) not in self.MAP_CHARS:
                    return (x, y), self.get(x, y)
        return None

    def is_out_of_bounds(self, x, y):
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def add_wall(self, x, y):
        self.map[(x, y)] = '#'

    def move_guard(self):
        guard_position, guard = self.find_guard()
        self.map[guard_position] = '.'
        direction = DIRECTIONS[guard]
        available_steps = [
            (guard_position[0] + n * direction[0], guard_position[1] + n * direction[1])
            for n in range(1, max(self.width, self.height))
        ]
        available_steps = [(x, y) for x, y in available_steps if not self.is_out_of_bounds(x, y)]
        object_on_path = [self.get(x, y) for x, y in available_steps]
        if "#" in object_on_path:
            available_steps = available_steps[:object_on_path.index("#")]
        n_visited = sum(self.visited.values())
        for step in available_steps:
            self.visited[step] = True
        if not available_steps or n_visited == sum(self.visited.values()):
            return None
        if self.is_out_of_bounds(
                *[available_steps[-1][0] + direction[0], available_steps[-1][1] + direction[1]]
        ):
            self.map[available_steps[-1]] = "."
            return None
        self.map[available_steps[-1]] = TURN_SEQUENCE[guard]
        self.move_guard()


if __name__ == "__main__":
    data_file = "data/example.dat"
    with open(data_file, "r") as f:
        map_data = [list(line.strip()) for line in f.readlines()]

    input_map = Map(map_data)
    input_map.move_guard()
    print(sum(input_map.visited.values()))

    n_positions = 0
    for x, y in input_map.visited:
        with open(data_file, "r") as f:
            map_data = [list(line.strip()) for line in f.readlines()]
        input_map = Map(map_data)
        if (x, y) == input_map.find_guard()[0]:
            continue
        if input_map.get(x, y) != "#":
            input_map.add_wall(x, y)
            input_map.move_guard()
        if input_map.find_guard():
            print(input_map.find_guard())
            n_positions += 1

    print(n_positions)