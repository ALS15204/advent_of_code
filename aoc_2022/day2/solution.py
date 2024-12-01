from pathlib import Path

from day2.utils import Rock, Paper, Scissor

SCRIPT_DIR = Path(__file__).parent
OPPONENT_TO_SHAPE = {"A": Rock, "B": Paper, "C": Scissor}
ME_TO_SHAPE = {"X": Rock, "Y": Paper, "Z": Scissor}
OUTCOME = {"X": "winner_to", "Y": "draw", "Z": "loser_to"}
LINE_ESCAPE = "\n"


if __name__ == "__main__":
    with open(SCRIPT_DIR / "input.dat", "r") as input_file:
        lines = input_file.readlines()
    lines = [line.replace(LINE_ESCAPE, "").split() for line in lines if line != LINE_ESCAPE]
    p1_points = [
        ME_TO_SHAPE[line[1]].point + ME_TO_SHAPE[line[1]].point_against(OPPONENT_TO_SHAPE[line[0]]) for line in lines
    ]
    print(f"Part One: Total points gained is {sum(p1_points)}.")

    p2_my_shape = [
        getattr(OPPONENT_TO_SHAPE[line[0]], OUTCOME[line[1]]) for line in lines
    ]
    p2_points = [
        my_shape.point + my_shape.point_against(
            OPPONENT_TO_SHAPE[line[0]]
        ) for (my_shape, line) in zip(p2_my_shape, lines)
    ]
    print(f"Part Two: Total points gained is {sum(p2_points)}")