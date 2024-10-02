from rubik.cube import Cube
from asymmetric_rubiks_cube.Logger import Logger
from asymmetric_rubiks_cube.Player import Player
from asymmetric_rubiks_cube.constants import SOLVED_CUBE_STR, SCRAMBLER, UNSCRAMBLER, NUM_SCRAMBLE_STEPS, \
    NUM_UNSCRAMBLE_STEPS, cube_to_numpy_array, SOLVED_REWARD, REPEATED_STATE_PENALTY


class RubiksCubeGame:
    def __init__(self):
        self.logger = Logger()
        self.state = Cube(SOLVED_CUBE_STR)
        self.players = [Player(SCRAMBLER), Player(UNSCRAMBLER)]
        self.current_player = SCRAMBLER
        self.is_game_over, self.step_num, self.current_reward = False, 0, 0

    def step(self, action):
        self.step_num += 1
        self.__perform_action(action)
        self.__set_is_game_over_reward()
        self.__switch_player()
        return cube_to_numpy_array(self.state), self.current_reward, self.is_game_over

    def reset(self):
        if not self.state.is_solved():
            self.logger.log_failed_state(self.__get_scrambler(), self.__get_unscrambler())
        self.__init__()
        return cube_to_numpy_array(self.state)

    def __perform_action(self, action):
        self.state = self.__get_current_player().perform_action(action, self.state, self.step_num)

    def __get_current_player(self):
        return self.players[self.current_player]

    def __set_is_game_over_reward(self):
        self.__set_game_over_reward(is_game_over=False, reward=0)
        if self.__is_solved_early():
            self.__set_reward_for_solved_early()
        elif self.__has_exceeded_num_steps():
            self.__set_game_over_reward_when_num_steps_exceeded()
        if self.__get_current_player().has_player_repeated_state(self.state):
            self.__set_game_over_reward(is_game_over=True, reward=REPEATED_STATE_PENALTY)

    def __set_reward_for_solved_early(self):
        if self.current_player == SCRAMBLER:
            self.__set_game_over_reward(is_game_over=True, reward=-1)
            self.logger.log_failed_state(self.__get_scrambler(), self.__get_unscrambler())
        else:
            self.__set_game_over_reward(is_game_over=True, reward=SOLVED_REWARD)

    def __set_game_over_reward_when_num_steps_exceeded(self):
        if self.current_player == UNSCRAMBLER:
            if not self.state.is_solved():
                self.__set_game_over_reward(is_game_over=True, reward=-1)
                self.logger.log_failed_state(self.__get_scrambler(), self.__get_unscrambler())
            else:
                self.__set_game_over_reward(is_game_over=True, reward=SOLVED_REWARD)
                self.logger.log_winning_state(self.__get_scrambler(), self.__get_unscrambler())

    def __set_game_over_reward(self, is_game_over, reward):
        self.__get_current_player().add_to_total_reward(reward)
        self.is_game_over, self.current_reward = is_game_over, reward

    def __switch_player(self):
        self.current_player = UNSCRAMBLER if self.current_player == SCRAMBLER else SCRAMBLER

    def __is_solved_early(self):
        return self.state.is_solved() and not self.__has_exceeded_num_steps()

    def __has_exceeded_num_steps(self):
        return self.step_num + 2 >= 2 * (NUM_SCRAMBLE_STEPS + NUM_UNSCRAMBLE_STEPS)

    def __get_scrambler(self):
        return self.players[SCRAMBLER]

    def __get_unscrambler(self):
        return self.players[UNSCRAMBLER]
