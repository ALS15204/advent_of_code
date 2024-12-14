from collections import Counter
from dataclasses import dataclass
from typing import Tuple
import math
import numpy as np
import re

from aoc_2024.day_12.garden_groups import find_clusters

WIDTH = 101
HEIGHT = 103
POSITION_VELOCITY_PATTERN = re.compile(r"p=(\d+),(\d+)\sv=(-?\d+),(-?\d+)")
TOTAL_TIME = 100
MIDPOINT = (WIDTH // 2, HEIGHT // 2)


def wrap_around(value, max_value):
    return value % (max_value + 1)


def initialize_robots(lines: list[str]) -> list["Robot"]:
    robots = []
    for line in lines:
        position_0, position_1, velocity_0, velocity_1 = map(int, POSITION_VELOCITY_PATTERN.match(line).groups())
        robots.append(Robot((position_0, position_1), (velocity_0, velocity_1)))
    return robots


def map_all_positions(robots: list["Robot"]) -> np.ndarray:
    robot_map = np.zeros((WIDTH, HEIGHT), dtype=int)
    for robot in robots:
        robot_map[robot.position] = 1
    return robot_map


@dataclass
class Robot:
    position: Tuple[int, int]
    velocity: Tuple[int, int]

    def move(self, time_step: int = 1):
        self.position = (
            wrap_around(self.position[0] + self.velocity[0] * time_step, WIDTH - 1),
            wrap_around(self.position[1] + self.velocity[1] * time_step, HEIGHT - 1),
        )

    @property
    def n_quadrant(self) -> int:
        if self.position[0] > MIDPOINT[0] and self.position[1] < MIDPOINT[1]:
            return 0
        elif self.position[0] < MIDPOINT[0] and self.position[1] < MIDPOINT[1]:
            return 1
        elif self.position[0] < MIDPOINT[0] and self.position[1] > MIDPOINT[1]:
            return 2
        elif self.position[0] > MIDPOINT[0] and self.position[1] > MIDPOINT[1]:
            return 3
        return 4


if __name__ == "__main__":
    with open("data/input.dat") as file:
        lines = file.read().splitlines()

    robots = initialize_robots(lines)

    for robot in robots:
        robot.move(TOTAL_TIME)
    quadrant_count = Counter([robot.n_quadrant for robot in robots])
    quadrant_count.pop(4)
    print(math.prod(quadrant_count.values()))

    robots = initialize_robots(lines)
    for n_sec in range(1000000000000000000):
        for robot in robots:
            robot.move()
        robot_map = map_all_positions(robots)
        clustered, n_cluster = find_clusters(robot_map)
        if n_cluster < len(robots) - 250:
            print(n_sec + 1)
