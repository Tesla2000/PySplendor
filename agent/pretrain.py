import operator
from collections import deque
from functools import reduce
from itertools import islice

import torch

from Config import Config
from agent.Agent import Agent
from agent.train_agent import train_agent


def pretrain(agents: deque[Agent]):
    for agent, checkpoint_index in zip(
        islice(reversed(agents), 1, None),
        sorted(
            (int(path.name.split(".")[0]) for path in Config.model_path.iterdir()),
            reverse=True,
        ),
    ):
        try:
            agent.load_state_dict(
                torch.load(Config.model_path.joinpath(f"{checkpoint_index}.pth"))
            )
        except RuntimeError:
            pass
    newest = Config.model_path.joinpath(
        f"{max((*tuple(int(path.name.split('.')[0]) for path in Config.model_path.iterdir()), 0))}.pth"
    )
    if newest.exists():
        try:
            agents[-1].load_state_dict(torch.load(newest))
        except RuntimeError:
            pass
    train_agent(agents[-1])

