import atexit
from collections import defaultdict, deque
from itertools import count, filterfalse
from operator import attrgetter
from statistics import fmean

import numpy as np
import torch
from torch import nn
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm

from Config import Config
from agent.SpeedAgent import SpeedAgent
from agent.SpeedRLDataset import SpeedRLDataset
from db.save_speed_sample import save_speed_sample
from src.Game import Game

agent = SpeedAgent()


def train_to_go_fast():
    train_buffer = deque(maxlen=10_000)
    loss_function = nn.MSELoss()
    optimizer = Adam(agent.parameters(), lr=1e-5)
    dataset = SpeedRLDataset(train_buffer)
    results_over_time = deque(maxlen=100)
    for epoch in count(1):
        agent.eval()
        games = [Game()]
        states = defaultdict(list)
        while True:
            games = list(filterfalse(Game.is_terminal, games))
            states = list(map(Game.get_state, games))
            with torch.no_grad():
                move_probs = agent(torch.tensor(states).float())
            move_indexes = np.argsort(move_probs)
            for move_index in move_indexes[0]:
                move = game.all_moves[move_index]
                if move.is_valid(game):
                    game = game.perform(move)
                    break
            states[game.current_player.id].append([state, move_index])
        for player in game.players:
            if player.points >= Config.min_n_points_to_finish:
                results_over_time.append(game.turn_counter / 2)
                train_buffer += ((state, move_till_end, int(move_index)) for move_till_end, (state, move_index) in
                                 enumerate(reversed(states[player.id]), 1))
            else:
                continue
                # train_buffer += ((state, 100, int(move_index)) for state, move_index in states[player.id])
        if not train_buffer:
            continue
        if epoch % 10 == 0:
            print(epoch, fmean(results_over_time))
        agent.train()
        loader = DataLoader(dataset, batch_size=128)
        for state, moves_till_end, move_indexes in loader:
            optimizer.zero_grad()
            outputs = agent(state)
            loss = sum(loss_function(output[move_index], move_till_end.float()) for move_index, move_till_end, output in
                       zip(move_indexes, moves_till_end, outputs))
            # print(loss.item())
            loss.backward()
            optimizer.step()


@atexit.register
def _save():
    torch.save(agent.state_dict(), Config.model_path.joinpath('speed_game.pth'))
