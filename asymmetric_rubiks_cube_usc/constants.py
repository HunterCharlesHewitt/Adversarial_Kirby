import datetime
import os

SOLVED_CUBE_STR = "OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR"
LEGAL_MOVES = ["L", "R", "U", "D", "F", "B", "Li", "Ri", "Ui", "Di", "Fi", "Bi"]
ACTIONS_RANGE = list(range(len(LEGAL_MOVES)))
MAX_NUM_STEPS = 5
DATE_AT_PROGRAM_START = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
