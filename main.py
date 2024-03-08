import random
import re
from collections import deque
from copy import deepcopy
from itertools import count

import torch

from Config import Config
from agent.Agent import Agent
from agent.pretrain import pretrain
from agent.save import save_temp_buffer
from agent.self_play import self_play
from agent.train_agent import train_agent


def main():
    training_buffer = deque(maxlen=Config.training_buffer_len)
    agents = deque(
        (Agent(Config.n_players) for _ in range(Config.n_players)),
        maxlen=Config.n_players,
    )
    if Config.pretrain:
        pretrain(agents)
    scores = deque(maxlen=Config.max_results_held)
    for _ in count() if Config.n_games is None else range(Config.n_games):
        buffer, winners = self_play(agents)
        to_train = random.random() > Config.eval_rate
        save_temp_buffer(buffer, to_train)
        for winner in winners:
            scores.append(agents[-1] is winner)
        if (
            len(scores) < Config.min_games_to_replace_agents
            and sum(scores)
            > Config.minimal_relative_agent_improvement
            * Config.min_games_to_replace_agents
            / len(agents)
        ) or (
            len(scores) > Config.min_games_to_replace_agents
            and sum(scores)
            >= Config.minimal_relative_agent_improvement * len(scores) / len(agents)
        ):
            torch.save(
                agents[-1].state_dict(),
                Config.model_path.joinpath(
                    str(
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
                    + ".pth"
                ),
            )
            agents.append(Agent(Config.n_players))
            agents[-1].load_state_dict(deepcopy(agents[-2].state_dict()))
            agents[-1].training = True
            scores = deque(maxlen=Config.max_results_held)
        elif len(scores) >= Config.min_games_to_replace_agents:
            print(f"{len(scores)} {sum(scores) / len(scores):.2f}")
        else:
            print(f"{len(scores)} {sum(scores)}/{len(scores)}")
        if to_train:
            training_buffer += buffer
            train_agent(agents[-1], training_buffer)


if __name__ == "__main__":
    main()
