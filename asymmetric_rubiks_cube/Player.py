from abc import abstractmethod

from asymmetric_rubiks_cube.constants import LEGAL_MOVES, NUM_SCRAMBLE_STEPS, UNSCRAMBLER


class Player:
    def __init__(self, player_type):
        self.total_reward = 0
        self.moves = ""
        self.visited_states = []
        self.steps_taken = 0
        self.player_type = player_type

    @abstractmethod
    def perform_action(self, action, state, step_num):
        if self.is_turn(step_num):
            self.moves += LEGAL_MOVES[action]
            self.visited_states.append(str(state))
            state.sequence(LEGAL_MOVES[action])
            self.steps_taken += 1
        return state

    def is_turn(self, step_num):
        if self.player_type == UNSCRAMBLER:
            return step_num >= 2 * NUM_SCRAMBLE_STEPS
        else:
            return step_num < 2 * NUM_SCRAMBLE_STEPS

    def has_state_been_visited(self, state):
        return str(state) in self.visited_states

    def add_to_total_reward(self, reward):
        self.total_reward += reward
