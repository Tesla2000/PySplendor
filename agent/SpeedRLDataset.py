from collections import deque

import torch
from torch.utils.data import Dataset

from Config import Config


class SpeedRLDataset(Dataset):
    def __init__(self, train_buffer: deque):
        self.train_buffer = train_buffer

    def __len__(self):
        return len(self.train_buffer)

    def __getitem__(self, item):
        state, moves, move_index = self.train_buffer[item]
        return torch.tensor(state).to(Config.device).float(), moves, move_index,
