import random
from pathlib import Path

import numpy as np
import torch


class _ConfigPaths:
    root = Path(__file__).parent
    training_data_path = root / "training_data"
    training_data_path.mkdir(exist_ok=True)
    evaluation_data_path = root / "evaluation_data"
    evaluation_data_path.mkdir(exist_ok=True)
    model_path = root / "models"
    model_path.mkdir(exist_ok=True)
    db_password = (root / "db_password").read_text().strip()


class _ConfigAgent:
    hidden_size = (
        256,
    )
    c = 0.5
    learning_rate = 5e-6
    debug = False
    pretrain = False
    # pretrain = True


class Config(_ConfigPaths, _ConfigAgent):
    dirichlet_alpha = .3
    dirichlet_epsilon = .25
    test_size = .2
    db_name = "splendor"
    train = True
    max_results_held = 100
    minimal_relative_agent_improvement = 1.1
    min_games_to_replace_agents = 40
    train_batch_size = 128
    training_buffer_len = 100_000
    min_n_points_to_finish = 15
    n_simulations = 100
    n_games = None
    n_players = 2
    n_actions = 45
    eval_rate = 0.2


if Config.debug:
    random.seed(42)
    np.random.seed(42)
    torch.random.manual_seed(42)
