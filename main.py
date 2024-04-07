import operator
import random
import re
from collections import deque
from copy import deepcopy
from functools import reduce
from itertools import count

import torch

from Config import Config
from agent.Agent import Agent
from agent.pretrain import pretrain
from agent.save import save_temp_buffer
from agent.self_play import self_play
from agent.train_agent import train_agent, eval_agent


def train_loop():
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


def evaluation():
    agent = Agent(Config.n_players)
    train_set = reduce(
        operator.add,
        (eval(path.read_text()) for path in Config.training_data_path.iterdir()),
    )
    eval_set = reduce(
        operator.add,
        (eval(path.read_text()) for path in Config.evaluation_data_path.iterdir()),
    )
    prev_bce, prev_cce = float("inf"), float("inf")
    while True:
        train_agent(agent, train_set)
        bce, cce = eval_agent(agent, eval_set)
        if bce >= prev_bce and cce >= prev_bce:
            break
        prev_bce = min(prev_bce, bce)
        prev_cce = min(prev_cce, cce)


# def evaluation():
#     v_agent = LogisticRegression()
#     p_agent = LogisticRegression()
#     train_set = reduce(
#         operator.add,
#         (eval(path.read_text()) for path in Config.training_data_path.iterdir()),
#     )
#     eval_set = reduce(
#         operator.add,
#         (eval(path.read_text()) for path in Config.evaluation_data_path.iterdir()),
#     )
#     v_agent.fit(tuple(sample[0] for sample in train_set), tuple(sample[2] for sample in train_set))
#     p_agent.fit(tuple(sample[0] for sample in train_set), np.argmax(np.array(tuple(sample[1] for sample in train_set)), axis=1))
#     print(
#         v_agent.score(tuple(sample[0] for sample in eval_set), tuple(sample[2] for sample in eval_set)),
#         p_agent.score(tuple(sample[0] for sample in eval_set), np.argmax(np.array(tuple(sample[1] for sample in eval_set)), axis=1)),
#     )


def main():
    if Config.train:
        train_loop()
    else:
        evaluation()


if __name__ == "__main__":
    main()
