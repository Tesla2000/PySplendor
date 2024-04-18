import random
from collections import deque
from contextlib import nullcontext
from copy import deepcopy
from itertools import count, compress

import numpy as np
import torch
from paretoset import paretoset
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sqlalchemy import func, select
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset

from Config import Config
from db.Game import Game
from db.Sample import Sample
from db.session import session
from .Agent import Agent
from .PretrainDataset import PretrainDataset
from .RLDataset import RLDataset


def train_agent(agent: Agent, train_data: deque[tuple[tuple, np.array, int]] = None):
    session.execute(select(Sample)).fetchall()
    n_games = session.query(func.max(Game.id)).scalar()
    train_indexes, test_indexes = train_test_split(range(n_games), test_size=Config.test_size)
    test_data = None
    results = []
    best_models = []
    no_improvement_counter = 0
    if train_data is None:
        train_data = PretrainDataset(train_indexes)
        test_data = PretrainDataset(test_indexes)
    else:
        train_data = RLDataset(train_data)
    for _ in count():
        agent.train()
        optimizer = optim.Adam(agent.parameters(), lr=Config.pretrain_learning_rate if test_data else Config.train_learning_rate)
        _loop(agent, train_data, optimizer)
        if test_data is None:
            return
        agent.eval()
        with torch.no_grad():
            result = _loop(agent, test_data)
        results.append(result)
        best_models.append(deepcopy(agent.state_dict()))
        results = np.array(results)
        pareto_set_mask = paretoset(results, use_numba=False)
        results = list(results[pareto_set_mask])
        best_models = list(compress(best_models, pareto_set_mask))
        if any(map(result.__eq__, results)):
            no_improvement_counter = 0
            continue
        no_improvement_counter += 1
        if no_improvement_counter == Config.no_improvement_limit:
            agent.load_state_dict(random.choice(best_models))
            return


def _loop(
    agent: Agent,
    dataset: Dataset,
    optimizer: optim.Optimizer = None,
    batch_size=Config.train_batch_size,
):
    is_optimizer = optimizer is not None
    categorical_cross_entropy = nn.CrossEntropyLoss()
    mse = nn.MSELoss()
    loader = DataLoader(dataset, batch_size=batch_size)
    for index, (state, policy, win_probability) in enumerate(loader):
        state, policy, win_probability = (
            state.float().to(Config.device),
            policy.float().to(Config.device),
            win_probability.float().to(Config.device),
        )
        if is_optimizer:
            optimizer.zero_grad()
        with (nullcontext() if is_optimizer else torch.no_grad()):
            output_policy, output_v = agent(state)
        bce = mse(output_v, win_probability)
        cce = categorical_cross_entropy(output_policy, policy)
        loss = bce + cce
        if is_optimizer:
            loss.backward()
            optimizer.step()
        else:
            print(
                round(accuracy_score(win_probability, np.sign(output_v.detach().numpy()).clip(0, 1)), 2),
                round(accuracy_score(
                    np.argmax(policy.detach().numpy(), axis=1),
                    np.argmax(output_policy.detach().numpy(), axis=1),
                ), 2),
            )
            return [bce.item(), cce.item()]
