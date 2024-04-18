import re

import torch

from Config import Config
from agent.Agent import Agent


def save_agent(agent: Agent):
    agent_number = str(
        max(
            map(
                int,
                (
                    *re.findall(
                        r"\d+",
                        "".join(map(str, Config.model_path.iterdir())),
                    ),
                    -1,
                ),
            )
        )
        + 1
    )
    torch.save(
        agent.state_dict(),
        Config.model_path.joinpath(
            agent_number
        ).with_suffix(".pth"),
    )
    Config.model_path.joinpath(
        agent_number
    ).with_suffix(".txt").write_text(str(agent.hidden_sizes))
