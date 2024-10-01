import time
import itertools
from muzero import MuZero
from games.asymmetric_rubiks_cube import MuZeroConfig
from dataclasses import dataclass


# Define a dataclass for configurations to easily manage configurations
@dataclass
class Config:
    num_workers: int = 2
    selfplay_on_gpu: bool = True
    network: str = "resnet"
    blocks: int = 1
    channels: int = 16
    optimizer: str = "Adam"
    batch_size: int = 128
    lr_init: float = 0.003


# List of possible values for each parameter to test
num_workers_options = [1, 2, 4, 8]
selfplay_on_gpu_options = [True, False]
network_options = ["resnet", "fullyconnected"]
blocks_options = [1, 2, 4]
channels_options = [16, 32, 64]
optimizer_options = ["Adam", "SGD"]
batch_size_options = [64, 128, 256]
lr_init_options = [0.003, 0.001, 0.0003]

# Create combinations of all options
configurations = list(itertools.product(num_workers_options, selfplay_on_gpu_options, network_options,
                                        blocks_options, channels_options, optimizer_options,
                                        batch_size_options, lr_init_options))


# Function to update the MuZeroConfig
def update_config(muzero_config, config):
    muzero_config.num_workers = config.num_workers
    muzero_config.selfplay_on_gpu = config.selfplay_on_gpu
    muzero_config.network = config.network
    muzero_config.blocks = config.blocks
    muzero_config.channels = config.channels
    muzero_config.optimizer = config.optimizer
    muzero_config.batch_size = config.batch_size
    muzero_config.lr_init = config.lr_init


# Function to measure the training time for 1000 steps
def measure_training_time(muzero_config):
    muzero = MuZero("rubiks_cube", config=muzero_config)
    print(muzero_config)
    start_time = time.time()
    muzero.train()
    end_time = time.time()
    print(end_time-start_time)
    return end_time - start_time


if __name__ == "__main__":
    # Run experiments
    results = []
    i = 0
    for config_values in configurations:
        print(f"Step {i}/{len(configurations)}")
        i = i + 1
        config = Config(*config_values)
        muzero_config = MuZeroConfig()
        update_config(muzero_config, config)
        time_taken = measure_training_time(muzero_config)
        results.append((config, time_taken))
        best_config, best_time = min(results, key=lambda x: x[1])
        print("Best Configuration So Far: ", best_config)
        print("Time Taken:", best_time)

    # Find the best configuration
    best_config, best_time = min(results, key=lambda x: x[1])

    print("Best Configuration: ", best_config)
    print("Time Taken:", best_time)

    # Print all results
    for config, time_taken in results:
        print(config, time_taken)
