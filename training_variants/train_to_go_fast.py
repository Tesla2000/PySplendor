import atexit
import re
from collections import deque
from dataclasses import dataclass
from itertools import count
from statistics import fmean

import numpy as np
import torch
from torch import nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from Config import Config
from agent.SpeedAgent import SpeedAgent
from agent.SpeedRLDataset import SpeedRLDataset
from src.Game import Game

agent = SpeedAgent()
agent.load_state_dict(torch.load(Config.model_path.joinpath('speed_game.pth')))


@dataclass
class GameState:
    game_instance: Game
    prev_state: "GameState" = None
    move_index: int = None


def _get_new_games(games: list[GameState], results_over_time: deque[float], beta: int, train_buffer):
    players = list(player.id for player in games[0].game_instance.players)
    move_log = []
    while True:
        games = list(game for game in games if not game.game_instance.is_terminal())
        if not games:
            print("No valid results")
            break
        game_states = list(game.game_instance.get_state() for game in games)
        with torch.no_grad():
            move_probs = agent(torch.tensor(game_states).float()).flatten().numpy()
        move_indexes = np.argsort(move_probs)
        new_games = []
        for move_index in move_indexes:
            game_index, move_index = divmod(move_index, Game.action_size)
            game = games[game_index]
            move = Game.all_moves[move_index]
            if move.is_valid(game.game_instance):
                game.move_index = move_index
                new_game = GameState(game.game_instance.perform(move), game)
                # if any(map(Config.min_n_points_to_finish.__le__, map(attrgetter("points"), new_game.game_instance.players))):
                if new_game.game_instance.players[-1].points >= Config.min_n_points_to_finish and (player_id := new_game.game_instance.players[-1].id) in players:
                    players.remove(player_id)
                    if not move_log:
                        results_over_time.append(new_game.game_instance.turn_counter / 2)
                    prev_state = new_game
                    # game_instances = []
                    for moves_till_end in count():
                        if prev_state is None:
                            break
                        if prev_state.game_instance.current_player.id == player_id:
                            move_log.append((prev_state.game_instance, prev_state.game_instance.all_moves[prev_state.move_index]))
                            train_buffer.append(
                                (prev_state.game_instance.get_state(), moves_till_end, prev_state.move_index))
                        prev_state = prev_state.prev_state
                            # game_instances.append(prev_state.game_instance)
                    if not players:
                        return
                new_games.append(new_game)
                if len(new_games) == beta:
                    break
        games = new_games


def train_to_go_fast():
    train_buffer = deque(maxlen=10_000)
    loss_function = nn.MSELoss()
    optimizer = Adam(agent.parameters(), lr=5e-7)
    dataset = SpeedRLDataset(train_buffer)
    results_over_time = deque(maxlen=100)
    beta = Config.beta
    for epoch in count(max(int(re.findall(r'\d+', path.name)[0]) for path in Config.model_path.glob("speed_game_*")) + 1):
        agent.eval()
        games = [GameState(Game())]
        _get_new_games(games, results_over_time, beta, train_buffer)
        if not train_buffer:
            continue
        if epoch % 1 == 0:
            print(epoch, fmean(results_over_time), sorted(results_over_time))
        if epoch % 1000 == 0:
            torch.save(agent.state_dict(),
                       Config.model_path.joinpath(f'speed_game_{epoch}_{fmean(results_over_time)}.pth'))
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


# @atexit.register
# def _save():
#     torch.save(agent.state_dict(), Config.model_path.joinpath('speed_game.pth'))
