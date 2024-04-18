from itertools import chain
from typing import Sequence

import numpy as np
from sqlalchemy import select
from torch.utils.data import Dataset

from agent.GameSample import GameSample
from db.Sample import Sample
from db.session import session


class PretrainDataset(Dataset):
    def __init__(self, indexes: Sequence[int]):
        self.indexes = indexes
        self.index_to_id = dict(enumerate(chain.from_iterable(session.execute(select(Sample.id).where(Sample.game_id.in_(self.indexes))).fetchall())))

    def __len__(self):
        return len(self.index_to_id)

    def __getitem__(self, index) -> GameSample:
        sample = session.execute(select(Sample).where(Sample.id == self.index_to_id[index])).scalar()
        return GameSample(
            np.array(sample.state),
            np.array(sample.policy),
            np.array([sample.outcome]),
        )
