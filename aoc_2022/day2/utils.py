from abc import ABC
from dataclasses import dataclass


@dataclass
class Shape(ABC):

    winner_to: "Shape"
    loser_to: "Shape"
    draw: "Shape"
    point: int

    @classmethod
    def point_against(cls, other: "Shape"):
        if other == cls.winner_to:
            return 6
        elif other == cls.loser_to:
            return 0
        else:
            return 3


class Rock(Shape):
    winner_to = None
    loser_to = None
    point = 1
    draw = None


class Paper(Shape):
    winner_to = Rock
    loser_to = None
    draw = None
    point = 2


class Scissor(Shape):
    winner_to = Paper
    loser_to = Rock
    draw = None
    point = 3


Scissor.draw = Scissor
Paper.loser_to = Scissor
Paper.draw = Paper
Rock.winner_to = Scissor
Rock.loser_to = Paper
Rock.draw = Rock
