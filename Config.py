import random

import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.random.manual_seed(42)


class Config:
    min_n_points_to_finish = 15
    n_simulations = 100
    n_games = 1
    n_players = 2
