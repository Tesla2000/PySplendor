import re
from collections import deque
from copy import deepcopy
from itertools import count
from pathlib import Path

import torch

from Config import Config
from agent.Agent import Agent
from agent.self_play import self_play
from agent.train_agent import train_agent


def main():
    training_buffer = deque(maxlen=Config.training_buffer_len)
    agents = deque((Agent(Config.n_players) for _ in range(Config.n_players)), maxlen=Config.n_players)
    if Config.pretrain:
        training_buffer += list(map(eval, map(Path.read_text, sorted(Config.data_path.iterdir(), key=lambda path: int(path.name), reverse=True)[:Config.training_buffer_len])))
        train_agent(agents[-1], training_buffer)
    scores = deque(maxlen=Config.max_results_held)
    for _ in (count() if Config.n_games is None else range(Config.n_games)):
        buffer, winner = self_play(agents)
        Config.data_path.joinpath(str(max((*tuple(int(path.name) for path in Config.data_path.iterdir()), -1)) + 1)).write_text(str((list(buffer[0][0]), list(buffer[0][1]), buffer[0][2])))
        scores.append(agents[-1] is winner)
        if len(scores) >= Config.min_games_to_replace_agents and sum(scores) > Config.minimal_relative_agent_improvement * len(scores) / len(agents):
            torch.save(agents[-1].state_dict(), Config.model_path.joinpath(str(max(map(int, (*re.findall(r'\d+', ''.join(map(str, Config.model_path.iterdir()))), -1))) + 1) + ".pth"))
            agents.append(Agent(Config.n_players).load_state_dict(deepcopy(agents[-1].state_dict())))
            agents[-1].training = True
            scores = deque(maxlen=Config.max_results_held)
        print(sum(scores) / len(scores), len(scores))
        training_buffer += buffer
        train_agent(agents[-1], training_buffer)


if __name__ == "__main__":
    main()
