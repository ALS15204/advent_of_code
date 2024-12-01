from pathlib import Path
from typing import List, Optional


SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / "example.dat"


class Component:
    def __init__(self, name, connections: Optional[List["Component"]]):
        self.name = name
        self._connections = connections or []

    def __repr__(self):
        return f"Component({self.name}, {self.connections})"

    def add_connectoin(self, connection: "Component"):
        if connection not in self._connections:
            self._connections.append(connection)

    @property
    def connections(self):
        return self._connections


def main():
    with open(INPUT_FILE) as f:
        data = f.read().splitlines()

    name_to_component = {}
    for line in data:
        name, connections = line.split(":")
        if name not in name_to_component:
            new_component = Component(name, [])
            name_to_component[name] = new_component
        else:
            new_component = name_to_component[name]
        for connection in connections.split():
            if connection not in name_to_component:
                name_to_component[connection] = Component(connection, [])
            new_component.add_connectoin(name_to_component[connection])
            name_to_component[connection].add_connectoin(new_component)
    pass


if __name__ == "__main__":
    main()
