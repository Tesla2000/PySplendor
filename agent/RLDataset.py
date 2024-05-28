from collections import deque

import torch
from torch.utils.data import Dataset

from Config import Config


class RLDataset(Dataset):
    def __init__(self):
        self.train_buffer = deque(maxlen=Config.training_buffer_len)

    def __len__(self):
        return len(self.train_buffer)

    def __getitem__(self, item):
        state, turns_till_end, move_index = self.train_buffer[item]
        return torch.tensor(state).to(Config.device).float(), turns_till_end, move_index,
