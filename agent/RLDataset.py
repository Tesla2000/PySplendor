from collections import deque

import numpy as np
from torch.utils.data import Dataset


class RLDataset(Dataset):
    def __init__(self, examples: deque[tuple[tuple, np.array, int]]):
        self.examples = examples

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index) -> tuple[np.array, ...]:
        return np.array(self.examples[index][0]), np.array(self.examples[index][1]), np.array(
            [self.examples[index][2] * 2 - 1])
