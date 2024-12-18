from math import sqrt


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)


def astar(maze, start, end):

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = set()
    closed_list = set()

    # Add the start node
    open_list.add(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list.pop()
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                open_list.add(current_node)
                current_node = item
                open_list.remove(item)

        # Pop current off open list, add to closed list
        closed_list.add(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = sqrt(
                (child.position[0] - end_node.position[0])**2 + (child.position[1] - end_node.position[1])**2
            )
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                continue
                # Add the child to the open list
            open_list.add(child)


def create_maze(filename, n_bytes, dimension):
    maze = [[0 for _ in range(dimension)] for _ in range(dimension)]
    with open(filename, "r") as file:
        for line_idx, line in enumerate(file.readlines(), 1):
            if line_idx > n_bytes:
                break
            row_idx, col_idx = map(int, line.strip().split(","))
            maze[col_idx][row_idx] = 1
    return maze, row_idx, col_idx


if __name__ == "__main__":
    n_bytes = 1024
    dimension = 71
    maze, _, _ = create_maze("data/input.dat", n_bytes, dimension)
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)

    path = astar(maze, start, end)
    print(len(path) - 1)

    with open("data/input.dat", "r") as file:
        file_length = len(file.readlines())

    for n_bytes in range(1024, file_length):
        maze, row_idx, col_idx = create_maze("data/input.dat", n_bytes + 1, dimension)
        path = astar(maze, start, end)
        if not path:
            print(f"{row_idx},{col_idx}")
            break
