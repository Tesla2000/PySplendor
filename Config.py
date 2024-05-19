import os
import random
from pathlib import Path

import numpy as np
import torch
from dotenv import load_dotenv
from lightning import seed_everything

load_dotenv()

class _DBConfig:
    db_name = os.getenv("POSTGRES_DB")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_username = os.getenv("POSTGRES_USER")
    db_url = f"postgresql://{db_username}:{db_password}@localhost:5432/{db_name}"


class _ConfigPaths:
    root = Path(__file__).parent
    training_data_path = root / "training_data"
    training_data_path.mkdir(exist_ok=True)
    evaluation_data_path = root / "evaluation_data"
    evaluation_data_path.mkdir(exist_ok=True)
    model_path = root / "models"
    model_path.mkdir(exist_ok=True)
    gui = root / "gui"
    templates = gui / "template"
    ai_weights = root / 'speed_game.pth'


class _ConfigAgent:
    hidden_size = (
        256,
        128,
        64,
        32,
        32,
        32,
        32,
        32,
        32,
    )
    c = 0.5
    train_learning_rate = 5e-5
    retrain_learning_rate = 1e-3
    random_state = 42
    debug = True
    # debug = False
    if not debug:
        random_state = random.randint(0, 2 ** 32)
        print(f"{random_state=}")


class Config(_ConfigPaths, _ConfigAgent, _DBConfig):
    agent_print_interval = 10
    results_over_time_counter = 100
    agent_save_interval = 1000
    play_beta = 10
    beta = 10
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dirichlet_alpha = .3
    dirichlet_epsilon = .25
    test_size = .2
    train = True
    training_buffer_len = 10_000
    min_n_points_to_finish = 15
    n_simulations = 1000
    n_games = None
    n_players = 2
    n_actions = 45


seed_everything(Config.random_state, workers=True)
random.seed(Config.random_state)
np.random.seed(Config.random_state)
