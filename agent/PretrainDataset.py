from itertools import chain
from typing import Sequence

import numpy as np
from sklearn.model_selection import train_test_split
from sqlalchemy import func, select
from torch.utils.data import Dataset

from db.Game import Game
from db.Sample import Sample
from db.session import session


class RLDataset(Dataset):
    def __init__(self, indexes: Sequence[int]):
        self.indexes = indexes
        self.n_moves = session.execute(func.count().where(Sample.game_id in self.indexes)).scalar()

    def __len__(self):
        return len(self.indexes)

    def __getitem__(self, index) -> tuple[np.array, ...]:
        select(Sample).where(Sample.id)
        return (
            np.array(self.examples[index][0]),
            np.array(self.examples[index][1]),
            np.array([self.examples[index][2] * 2 - 1]),
        )
