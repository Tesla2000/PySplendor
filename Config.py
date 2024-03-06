import random

import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.random.manual_seed(42)


class Config:
    n_simulations = 1000
    n_games = 100
    n_players = 2
