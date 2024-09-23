import random

import numpy
from rubik.cube import Cube

from games.abstract_game import AbstractGame
from asymmetric_rubiks_cube_usc.constants import SOLVED_CUBE_STR, LEGAL_MOVES, ACTIONS_RANGE, MAX_NUM_STEPS, \
    DATE_AT_PROGRAM_START, FOLDER_PATH

NUM_TO_UNSCRAMBLE = 10
NUM_TO_SCRAMBLE = 2

class Game(AbstractGame):
    def __init__(self, seed=None):
        self.__set_new_game_state()

    def __set_new_game_state(self):
        self.unscramble_moves = ""
        self.scramble_moves = ""
        self.scrambled_cube_states = []
        self.unscrambled_cube_states = []
        self.player = 0
        self.scrambler_total_reward = 0
        self.unscrambler_total_reward = 0
        self.state = Cube(SOLVED_CUBE_STR)
        self.step_num = 0

    def step(self, action):
        if self.step_num >= NUM_TO_UNSCRAMBLE + NUM_TO_SCRAMBLE:
            if self.player == 1:
                print(f"Switching player after {self.step_num} steps")
                self.__switch_player()
                return self.__finish_step(reward=0, is_game_finished=False)
            else:
                return self.__finish_step(reward=1, is_game_finished=True)
        if self.player == 0:  # scrambler
            self.__perform_scramble(action)
            if self.state.is_solved():
                return self.__finish_step(reward=-10, is_game_finished=True)
            if self.__scrambled_state_has_already_been_visited():
                return self.__finish_step(reward=-1, is_game_finished=False)
            return self.__finish_step(reward=1, is_game_finished=False)
        else:  # unscrambler
            self.__perform_unscramble(action)
            if self.__unscrambled_state_has_already_been_visited():
                return self.__finish_step(reward=-1, is_game_finished=False)
            if self.state.is_solved():
                return self.__finish_step(reward=self.calculate_discounted_reward(), is_game_finished=True)
            return self.__finish_step(reward=0, is_game_finished=False)

    def calculate_discounted_reward(self):
        return 10 #max(1, 1 / (self.step_num - (NUM_TO_SCRAMBLE - 1)))

    def __finish_step(self, reward, is_game_finished):
        if self.player == 0:
            self.scrambler_total_reward += reward
            if self.scrambler_total_reward <= -10:
                is_game_finished = True
        else:
            self.unscrambler_total_reward += reward
            if self.unscrambler_total_reward <= -10:
                is_game_finished = True
            if is_game_finished:
                self.__log_winning_state()

        self.step_num += 1
        # I think this is the problem, we shouldn't be switching before they receive the reward
        if self.step_num == NUM_TO_SCRAMBLE:
            self.__switch_player()



        return self.__cube_to_numpy_array(), reward, is_game_finished

    def reset(self):
        if not self.state.is_solved():
            self.__log_failed_state()
        self.__set_new_game_state()
        return self.__cube_to_numpy_array()

    def render(self):
        print(remove_all_whitespace(self.state))

    def to_play(self):
        return self.player

    def legal_actions(self):
        return ACTIONS_RANGE

    def __has_game_exceeded_max_num_steps(self):
        return len(self.scramble_moves) >= MAX_NUM_STEPS

    def __perform_scramble(self, action):
        self.scramble_moves += LEGAL_MOVES[action]
        self.scrambled_cube_states.append(str(self.state))
        self.state.sequence(LEGAL_MOVES[action])

    def __perform_unscramble(self, action):
        self.unscramble_moves += LEGAL_MOVES[action]
        self.unscrambled_cube_states.append(str(self.state))
        self.state.sequence(LEGAL_MOVES[action])

    def __log_winning_state(self):
        with open(f"{FOLDER_PATH}/logs/winning_paths/winning_paths{DATE_AT_PROGRAM_START}.txt", "a") as myfile:
            self.__log_moves_taken(myfile)
        print(f"WON| Scrambler reward: {self.scrambler_total_reward} | Unscrambler reward: {self.unscrambler_total_reward}")

    def __log_failed_state(self):
        with open(f"{FOLDER_PATH}/logs/failed_paths/failed_paths{DATE_AT_PROGRAM_START}.txt", "a") as myfile:
            self.__log_moves_taken(myfile)

    def __log_moves_taken(self, myfile):
        scramble_moves = f"Scramble Moves: {self.scramble_moves} - Unscramble Moves: {self.unscramble_moves} \n"
        scrambler_reward = f"Scrambler Reward: {self.scrambler_total_reward} \n"
        unscrambler_reward = f"Unscrambler Reward: {self.unscrambler_total_reward} \n\n"
        myfile.write(scramble_moves + scrambler_reward + unscrambler_reward)

    def __cube_to_numpy_array(self):
        c = "".join(str(self.state).split())
        c = [ord(char) for char in c]
        front_face = numpy.array([[c[12], c[13], c[14]], [c[24], c[25], c[26]], [c[36], c[37], c[38]]])
        back_face = numpy.array([[c[18], c[19], c[20]], [c[30], c[31], c[32]], [c[42], c[43], c[44]]])
        right_face = numpy.array([[c[15], c[16], c[17]], [c[27], c[28], c[29]], [c[39], c[40], c[41]]])
        left_face = numpy.array([[c[9], c[10], c[11]], [c[21], c[22], c[23]], [c[33], c[34], c[35]]])
        top_face = numpy.array([[c[0], c[1], c[2]], [c[3], c[4], c[5]], [c[6], c[7], c[8]]])
        bottom_face = numpy.array([[c[45], c[46], c[47]], [c[48], c[49], c[50]], [c[51], c[52], c[53]]])
        return numpy.array([top_face, left_face, front_face, right_face, back_face, bottom_face])

    def __scrambled_state_has_already_been_visited(self):
        return str(self.state) in self.scrambled_cube_states

    def __unscrambled_state_has_already_been_visited(self):
        return str(self.state) in self.unscrambled_cube_states

    def __switch_player(self):
        self.player = 1 ^ self.player

    def human_to_action(self):
        while True:
            options = ', '.join([f"{int_move}: {char_move}" for int_move, char_move in enumerate(LEGAL_MOVES)])
            if self.player == 0:
                print("Try to scramble the cube")
            else:
                print("Try to unscramble the cube")
            choice = str(input(f"Enter one of the following moves: {options} \n"))
            if int(choice) in range(len(LEGAL_MOVES)):
                return int(choice)
            print("Wrong input, try again")


def remove_all_whitespace(string):
    return "".join(str(string).split())
