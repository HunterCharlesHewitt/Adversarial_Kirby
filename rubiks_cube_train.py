from muzero import MuZero

muzero = MuZero("rubiks_cube")
muzero.train()
muzero.test(render=True)