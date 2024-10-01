import os
import datetime


class Logger:
    folder_path = os.path.dirname(os.path.abspath(__file__))
    date_at_program_start = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")

    def log_winning_state(self, scrambler, unscrambler):
        with open(f"{self.folder_path}/logs/winning_paths/winning_paths{self.date_at_program_start}.txt", "a") as file:
            self.__log_moves_taken(file, scrambler, unscrambler)

    def log_failed_state(self, scrambler, unscrambler):
        with open(f"{self.folder_path}/logs/failed_paths/failed_paths{self.date_at_program_start}.txt", "a") as file:
            self.__log_moves_taken(file, scrambler, unscrambler)

    def __log_moves_taken(self, file, scrambler, unscrambler):
        scramble_moves = f"Scramble Moves: {scrambler.moves} - Unscramble Moves: {unscrambler.moves} \n"
        scrambler_reward_str = f"Scrambler Reward: {scrambler.total_reward} \n"
        unscrambler_reward_str = f"Unscrambler Reward: {unscrambler.total_reward} \n\n"
        file.write(scramble_moves + scrambler_reward_str + unscrambler_reward_str)
