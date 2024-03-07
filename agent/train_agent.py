import numpy as np
from torch import nn, optim
from torch.utils.data import DataLoader

from Config import Config
from src.Game import Game
from .Agent import Agent
from .RLDataset import RLDataset


def train_agent(agent: Agent, train_data: list[tuple[Game, np.array, int]]):
    agent.train()
    categorical_cross_entropy = nn.CrossEntropyLoss()
    binary_cross_entropy = nn.BCELoss()
    policy_optimizer = optim.Adam(agent.parameters())
    v_optimizer = optim.Adam(agent.parameters())
    dataset = RLDataset(train_data)
    loader = DataLoader(dataset, batch_size=Config.train_batch_size)
    for batch in loader:
        output_policy, output_v = agent(batch)
