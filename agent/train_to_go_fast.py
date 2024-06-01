import logging
import random
import re
import warnings
from collections import deque
from contextlib import suppress, redirect_stdout
from itertools import count
from statistics import fmean

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from Config import Config
from agent.Agent import Agent
from agent.RLDataset import RLDataset
from agent.entities import NoValidMove
from agent.get_shortest_games import get_shortest_games
from agent.services.game_end_checker import GameEndChecker, EndOnFirstPlayer
from agent.services.trianing_buffer_extender import TrainingBufferExtender, \
    TrainingBufferExtenderBestPlayer
from src.Game import Game

warnings.filterwarnings("ignore")
logging.getLogger("pytorch_lightning").setLevel(logging.WARNING)
agent = Agent()
last_saved_epoch = 0
with suppress(ValueError):
    last_saved_epoch = max(int(re.findall(r'\d+', path.name)[0]) for path in
                           Config.model_path.glob("speed_game_*"))
    agent.load_state_dict(torch.load(
        next(Config.model_path.glob(f'speed_game_{last_saved_epoch}*'))))


def _train_epoch(beta: int, results_over_time: deque[float],
                 train_dataset: RLDataset, epoch: int,
                 training_buffer_extender: TrainingBufferExtender,
                 game_end_checker: GameEndChecker):
    agent.eval()
    root = Game()
    try:
        shortest_games = get_shortest_games(root, game_end_checker, beta,
                                            agent)
    except NoValidMove:
        return
    shortest_game = random.choice(shortest_games)
    results_over_time.append(len(shortest_game) / 2)
    training_buffer_extender.append_to_buffer(train_dataset.train_buffer,
                                              shortest_game)
    if epoch % Config.agent_print_interval == 0:
        with redirect_stdout(Config.train_values_file):
            print(epoch, fmean(results_over_time), sorted(results_over_time),
                  flush=True)
    if epoch % Config.agent_save_interval == 0:
        torch.save(agent.state_dict(),
                   Config.model_path.joinpath(
                       f'speed_game_{epoch}_{fmean(results_over_time)}.pth'))
    train_loader = DataLoader(train_dataset, batch_size=128)
    pl.Trainer(max_epochs=1).fit(agent, train_loader)


def train_to_go_fast():
    train_buffer = RLDataset()
    results_over_time = deque(maxlen=Config.results_over_time_counter)
    beta = Config.beta
    training_buffer_extender = TrainingBufferExtenderBestPlayer()
    game_end_checker = EndOnFirstPlayer()
    for epoch in tqdm(count(last_saved_epoch + 1), "Training...", colour="blue"):
        _train_epoch(beta, results_over_time, train_buffer, epoch, training_buffer_extender, game_end_checker)
