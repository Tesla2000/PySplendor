import random
from pathlib import Path

import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.random.manual_seed(42)


class _ConfigPaths:
    root = Path(__file__).parent
    data_path = root / 'data'
    data_path.mkdir(exist_ok=True)
    model_path = root / 'models'
    model_path.mkdir(exist_ok=True)


class Config(_ConfigPaths):
    minimal_relative_agent_improvement = 1.1
    min_games_to_replace_agents = 20
    train_batch_size = 64
    training_buffer_len = 1000
    min_n_points_to_finish = 15
    n_simulations = 100
    n_games = None
    n_players = 2
    n_actions = 46
