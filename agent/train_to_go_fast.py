import logging
import random
import re
import sys
import warnings
from collections import deque
from itertools import count
from statistics import fmean

import pytorch_lightning as pl
import torch
from torch.utils.data import DataLoader

from Config import Config
from agent.Agent import Agent
from agent.RLDataset import RLDataset
from agent.get_shortest_game import get_shortest_game, GameSequence, GameState
from agent.services.game_end_checker import EndOnSecondPlayer, GameEndChecker
from src.Game import Game

warnings.filterwarnings("ignore")
logging.getLogger("pytorch_lightning").setLevel(logging.WARNING)
last_saved_epoch = max(int(re.findall(r'\d+', path.name)[0]) for path in Config.model_path.glob("speed_game_*"))
agent = Agent()
agent.load_state_dict(torch.load(next(Config.model_path.glob(f'speed_game_{last_saved_epoch}*'))))


def get_shortest_games(root: Game, game_end_checker: GameEndChecker, beta: int) -> list[GameSequence]:
    shortest_game_length = sys.maxsize
    shorted_games = []
    for shortest_game in get_shortest_game(GameState(root, None), beta, game_end_checker, agent):
        if len(shortest_game) <= shortest_game_length:
            shortest_game_length = len(shortest_game)
        else:
            break
        shorted_games.append(shortest_game)
    return shorted_games


def train_to_go_fast():
    train_buffer = RLDataset()
    trainer = pl.Trainer(max_epochs=1)
    results_over_time = deque(maxlen=100)
    beta = Config.beta
    for epoch in count(last_saved_epoch + 1):
        agent.eval()
        root = Game()
        game_end_checker = EndOnSecondPlayer(root)
        shortest_games = get_shortest_games(root, game_end_checker, beta)
        if not shortest_games:
            continue
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
