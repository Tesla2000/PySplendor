from typing import Sequence

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sqlalchemy import func, select
from torch import nn, optim
from torch.utils.data import DataLoader

from Config import Config
from db.Game import Game
from db.Sample import Sample
from db.session import session
from .Agent import Agent
from .RLDataset import RLDataset


def train_agent(agent: Agent):
    session.execute(select(Sample)).fetchall()
    n_games = session.query(func.max(Game.id)).scalar()
    train_indexes, test_indexes = train_test_split(range(n_games), test_size=Config.test_size)
    RLDataset(test_indexes)
    agent.train()
    optimizer = optim.Adam(agent.parameters(), lr=Config.learning_rate)
    _loop(agent, train_data, optimizer)


def eval_agent(agent: Agent, eval_set: Sequence[tuple[tuple, np.array, int]]):
    agent.eval()
    return _loop(agent, eval_set, batch_size=len(eval_set))


def _loop(
    agent: Agent,
    dataset: Sequence[tuple[tuple, np.array, int]],
    optimizer: optim.Optimizer = None,
    batch_size=Config.train_batch_size,
):
    is_optimizer = optimizer is not None
    categorical_cross_entropy = nn.CrossEntropyLoss()
    mse = nn.MSELoss()
    dataset = RLDataset(dataset)
    loader = DataLoader(dataset, batch_size=batch_size)
    for index, (state, policy, win_probability) in enumerate(loader):
        state, policy, win_probability = (
            state.float(),
            policy.float(),
            win_probability.float(),
        )
        if is_optimizer:
            optimizer.zero_grad()
        output_policy, output_v = agent(state)
        bce = mse(output_v, win_probability)
        cce = categorical_cross_entropy(output_policy, policy)
        if is_optimizer:
            bce.backward(retain_graph=True)
            cce.backward()
            optimizer.step()
        else:
            print(
                accuracy_score(win_probability, np.sign(output_v.detach().numpy())),
                accuracy_score(
                    np.argmax(policy.detach().numpy(), axis=1),
                    np.argmax(output_policy.detach().numpy(), axis=1),
                ),
            )
            return bce.item(), cce.item()
