from asymmetric_rubiks_cube.RubiksCubeGame import RubiksCubeGame
from asymmetric_rubiks_cube.constants import SCRAMBLER, LEGAL_MOVES, ACTIONS_RANGE
from games.abstract_game import AbstractGame


class Game(AbstractGame):
    def __init__(self, seed=None):
        self.rubiks_cube_game = RubiksCubeGame()

    def step(self, action):
        return self.rubiks_cube_game.step(action)

    def to_play(self):
        return self.rubiks_cube_game.current_player

    def reset(self):
        return self.rubiks_cube_game.reset()

    def legal_actions(self):
        return ACTIONS_RANGE

    def render(self):
        print(remove_all_whitespace(self.rubiks_cube_game.state))

    def human_to_action(self):
        while True:
            goal = "scramble" if SCRAMBLER == self.rubiks_cube_game.current_player else "unscramble"
            choice = input(f"Enter one of the following moves: {LEGAL_MOVES} in order to {goal} the cube:")
            if choice in LEGAL_MOVES:
                print("You chose {}".format(LEGAL_MOVES.index(choice)))
                return LEGAL_MOVES.index(choice)
            print("Wrong input, try again.\n")


def remove_all_whitespace(string):
    return "".join(str(string).split())
