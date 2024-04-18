from collections import deque
from itertools import starmap

from sqlalchemy import select, desc

from Config import Config
from agent.GameSample import GameSample
from db.Sample import Sample
from db.session import session


def load_train_buffer(n_samples: int = Config.training_buffer_len) -> deque[GameSample]:
    return deque(starmap(GameSample, session.execute(
        select(Sample.state, Sample.policy, Sample.outcome).order_by(desc(Sample.id)).limit(n_samples)).fetchall()),
                 maxlen=n_samples)
