import dataclasses
import itertools
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_DATA = SCRIPT_DIR / "input.dat"

MIN = 200000000000000
MAX = 400000000000000


@dataclasses.dataclass
class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


@dataclasses.dataclass
class Initial:
    def __init__(self, p: Vector, v: Vector):
        self.p = p
        self.v = v


def find_crossing(initial_1: Initial, initial_2: Initial) -> Vector:
    factor_y = (initial_2.p.y - initial_1.p.y) / (initial_1.v.y)
    factor_x = (initial_2.p.x - initial_1.p.x) / (initial_1.v.x)
    vx_ratio = initial_2.v.x / initial_1.v.x
    vy_ratio = initial_2.v.y / initial_1.v.y
    if vx_ratio == vy_ratio:
        return None
    t2 = (factor_y - factor_x) / (vx_ratio - vy_ratio)
    t1 = factor_x + vx_ratio * t2
    if t2 < 0 or t1 < 0:
        return None
    return Vector(initial_2.p.x + initial_2.v.x * t2, initial_2.p.y + initial_2.v.y * t2, 0)


def main():
    with open(INPUT_DATA) as f:
        data = f.read().splitlines()

    initial_list = []
    for line in data:
        p_str, v_str = line.split("@")
        p = Vector(*p_str.strip().split(","))
        v = Vector(*v_str.strip().split(","))
        initial_list.append(Initial(p, v))

    count = 0
    for i_1, i_2 in itertools.combinations(initial_list, 2):
        cross = find_crossing(i_1, i_2)
        if cross and cross.x > MIN and cross.x < MAX and cross.y > MIN and cross.y < MAX:
            count += 1
    print(count)


if __name__ == "__main__":
    main()  