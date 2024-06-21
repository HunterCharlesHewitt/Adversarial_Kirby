import datetime
import os

SOLVED_CUBE_STR = "OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR"

DATE_AT_PROGRAM_START = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))

SCRAMBLE_MOVES = ["Li", "Ri", "Ui", "Di", "Fi", "Bi", "Mi", "Ei", "Si"]
LEGAL_MOVES = ["L", "R", "U", "D", "F", "B", "M", "E", "S"]
ACTIONS_RANGE = list(range(len(LEGAL_MOVES)))
MAX_NUM_STEPS = 40
