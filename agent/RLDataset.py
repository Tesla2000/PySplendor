from collections import deque
from itertools import dropwhile
from operator import attrgetter

import torch
from torch.utils.data import Dataset

from Config import Config
from agent.entities import GameMovePairs
from src.Game import Game


class RLDataset(Dataset):
    def __init__(self):
        self.train_buffer = deque(maxlen=Config.training_buffer_len)

    def __len__(self):
        return len(self.train_buffer)

    def __getitem__(self, item):
        state, turns_till_end, move_index = self.train_buffer[item]
        return torch.tensor(state).to(Config.device).float(), turns_till_end, move_index,

    def append(self, game_sequence: GameMovePairs):
        player_ids = list(map(attrgetter("id"), game_sequence[0][0].players))
        for player_id in player_ids:
            for turns_till_end, (game, move) in enumerate(
                dropwhile(lambda game_state: game_state.game.current_player.points >= Config.min_n_points_to_finish,
                          filter(lambda game_state: game_state.game.current_player.id == player_id and game_state.move,
                                 game_sequence))):
                self.train_buffer.append((game.get_state(), turns_till_end, Game.all_moves.index(move)))
