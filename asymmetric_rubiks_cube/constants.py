import numpy

SOLVED_CUBE_STR = "OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR"
LEGAL_MOVES = ["L", "R", "U", "D", "F", "B", "Li", "Ri", "Ui", "Di", "Fi", "Bi"]
ACTIONS_RANGE = list(range(len(LEGAL_MOVES)))
SCRAMBLER = 0
UNSCRAMBLER = 1
NUM_SCRAMBLE_STEPS = 2
NUM_UNSCRAMBLE_STEPS = 2
SOLVED_REWARD = 1

def cube_to_numpy_array(state):
    c = "".join(str(state).split())
    c = [ord(char) for char in c]
    front_face = numpy.array([[c[12], c[13], c[14]], [c[24], c[25], c[26]], [c[36], c[37], c[38]]])
    back_face = numpy.array([[c[18], c[19], c[20]], [c[30], c[31], c[32]], [c[42], c[43], c[44]]])
    right_face = numpy.array([[c[15], c[16], c[17]], [c[27], c[28], c[29]], [c[39], c[40], c[41]]])
    left_face = numpy.array([[c[9], c[10], c[11]], [c[21], c[22], c[23]], [c[33], c[34], c[35]]])
    top_face = numpy.array([[c[0], c[1], c[2]], [c[3], c[4], c[5]], [c[6], c[7], c[8]]])
    bottom_face = numpy.array([[c[45], c[46], c[47]], [c[48], c[49], c[50]], [c[51], c[52], c[53]]])
    return numpy.array([top_face, left_face, front_face, right_face, back_face, bottom_face])