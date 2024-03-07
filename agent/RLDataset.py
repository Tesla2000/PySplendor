import numpy as np
from torch.utils.data import Dataset


class RLDataset(Dataset):
    def __init__(self, examples: list[tuple[np.array, np.array, int]]):
        self.examples = examples

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index) -> tuple[np.array, np.array, int]:
        return self.examples[index][0]
