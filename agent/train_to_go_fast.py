import logging
import random
import re
import warnings
from collections import deque
from contextlib import suppress
from itertools import count
from statistics import fmean

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader

from Config import Config
from agent.Agent import Agent
from agent.RLDataset import RLDataset
from agent.entities import NoValidMove
from agent.get_shortest_games import get_shortest_games
from agent.services.game_end_checker import EndOnSecondPlayer
from src.Game import Game

warnings.filterwarnings("ignore")
logging.getLogger("pytorch_lightning").setLevel(logging.WARNING)
last_saved_epoch = max(int(re.findall(r'\d+', path.name)[0]) for path in Config.model_path.glob("speed_game_*"))
agent = Agent()
agent.load_state_dict(torch.load(next(Config.model_path.glob(f'speed_game_{last_saved_epoch}*'))))


def _train_epoch(beta: int, results_over_time: deque[float], train_buffer: RLDataset, epoch: int, trainer: pl.Trainer):
    agent.eval()
    root = Game()
    game_end_checker = EndOnSecondPlayer()
    with suppress(NoValidMove):
        shortest_games = get_shortest_games(root, game_end_checker, beta, agent)
    if not shortest_games:
        return
    shortest_game = random.choice(shortest_games)
    results_over_time.append(len(shortest_game) / 2)
    train_buffer.append(shortest_game)
    if epoch % 1 == 0:
        print(epoch, fmean(results_over_time), sorted(results_over_time))
    if epoch % 1000 == 0:
        torch.save(agent.state_dict(),
                   Config.model_path.joinpath(f'speed_game_{epoch}_{fmean(results_over_time)}.pth'))
    train_loader = DataLoader(train_buffer, batch_size=128, num_workers=4)
    trainer.fit(agent, train_loader)


def train_to_go_fast():
    train_buffer = RLDataset()
    trainer = pl.Trainer(max_epochs=1)
    results_over_time = deque(maxlen=100)
    beta = Config.beta
    for epoch in count(last_saved_epoch + 1):
        _train_epoch(beta, results_over_time, train_buffer, epoch, trainer)
