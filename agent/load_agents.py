from collections import deque
from itertools import chain, repeat, islice

import torch

from Config import Config
from agent.Agent import Agent

from agent.train_agent import train_agent


def load_agents(pretrain: bool = Config.pretrain) -> deque[Agent]:
    agents = deque(islice(map(_load_agent, chain.from_iterable((sorted(
        (int(path.name.split(".")[0]) for path in Config.model_path.iterdir()),
        reverse=True,
    ), repeat(-1)))), Config.n_players), maxlen=Config.n_players)
    if pretrain:
        train_agent(agents[-1])
    return agents


def _load_agent(agent_number: int) -> Agent:
    if agent_number == -1:
        agent = Agent(Config.n_players)
        agent.to(Config.device)
        return agent
    agent_number = str(agent_number)
    hidden_size = eval(Config.model_path.joinpath(
        agent_number
    ).with_suffix(".txt").read_text())
    agent = Agent(Config.n_players, hidden_size)
    agent.load_state_dict(torch.load(
        Config.model_path.joinpath(
            agent_number
        ).with_suffix(".pth"),
    ))
    agent.to(Config.device)
    return agent
