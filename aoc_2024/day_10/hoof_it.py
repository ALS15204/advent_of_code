from collections import Counter

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, value, parent=None, position=None, children=None):
        self.value = value
        self.parent = parent
        self.position = position
        self.children = children or []

    def __eq__(self, other):
        return self.path == other.path

    def __repr__(self):
        return "->".join(map(str, self.path))

    @property
    def path(self):
        path = [self.position]
        node = self
        while node.parent:
            path.append(node.parent.position)
            node = node.parent
        return path[::-1]

    def search_by_length(self, length):
        paths = []
        if len(self.path) == length:
            paths.append(self.path)
        for child in self.children:
            paths.extend(child.search_by_length(length))
        return paths

    def add_parent(self, parent):
        assert self.parent is None
        self.parent = parent
        if self not in parent.children:
            parent.add_child(self)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
        if not child.parent:
            child.add_parent(self)


def take_steps(node, map_dict):
    if node.value == 9:
        return node
    x, y = node.position
    for dx, dy in [UP, DOWN, LEFT, RIGHT]:
        new_pos = (x + dx, y + dy)
        if new_pos in map_dict and map_dict[new_pos] == node.value + 1:
            new_node = Node(map_dict[new_pos], position=new_pos)
            node.add_child(new_node)
            take_steps(new_node, map_dict)
        else:
            continue


if __name__ == "__main__":
    with open("data/example.dat", "r") as f:
        map_dict = {}
        for row, line in enumerate(f.readlines()):
            for col, char in enumerate(line.strip()):
                map_dict[(col, row)] = int(char)

    trail_heads = [Node(0, position=key) for key, value in map_dict.items() if value == 0]


