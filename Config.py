import random
from pathlib import Path

import numpy as np
import torch


class _ConfigPaths:
    root = Path(__file__).parent
    training_data_path = root / 'training_data'
    training_data_path.mkdir(exist_ok=True)
    evaluation_data_path = root / 'evaluation_data'
    evaluation_data_path.mkdir(exist_ok=True)
    model_path = root / 'models'
    model_path.mkdir(exist_ok=True)


class _ConfigAgent:
    # hidden_sizes = (256, 128, 64, 32)
    hidden_sizes = (256,)
    # hidden_sizes = tuple()
    c = .1
    learning_rate = 1e-3
    debug = False
    pretrain = True


class Config(_ConfigPaths, _ConfigAgent):
    max_results_held = 100
    minimal_relative_agent_improvement = 1.1
    min_games_to_replace_agents = 40
    train_batch_size = 64
    training_buffer_len = 100_000
    min_n_points_to_finish = 15
    n_simulations = 100
    n_games = None
    n_players = 2
    n_actions = 46


if Config.debug:
    random.seed(42)
    np.random.seed(42)
    torch.random.manual_seed(42)
