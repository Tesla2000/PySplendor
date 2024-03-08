import re
from collections import deque
from copy import deepcopy
from itertools import count, islice
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
        for agent, checkpoint_index in zip(islice(reversed(agents), 1, None), sorted((int(path.name.split('.')[0]) for path in Config.model_path.iterdir()), reverse=True)):
            agent.load_state_dict(torch.load(Config.model_path.joinpath(f'{checkpoint_index}.pth')))
        newest = Config.model_path.joinpath(
            f"{max((*tuple(int(path.name.split('.')[0]) for path in Config.model_path.iterdir()), 0))}.pth")
        if newest.exists():
            agents[-1].load_state_dict(torch.load(newest))
        training_buffer += list(map(eval, map(Path.read_text, sorted(Config.training_data_path.iterdir(), key=lambda path: int(path.name), reverse=True)[:Config.training_buffer_len])))
        train_agent(agents[-1], training_buffer)
    scores = deque(maxlen=Config.max_results_held)
    for _ in (count() if Config.n_games is None else range(Config.n_games)):
        buffer, winners = self_play(agents)
        start_index = max((*tuple(int(path.name) for path in Config.training_data_path.iterdir()), -1)) + 1
        for start_index, sample in enumerate(buffer, start_index + 1):
            Config.training_data_path.joinpath(str(start_index)).write_text(str((list(sample[0]), list(sample[1]), sample[2])))
        for winner in winners:
            scores.append(agents[-1] is winner)
        if (len(scores) < Config.min_games_to_replace_agents and sum(scores) >= Config.minimal_relative_agent_improvement * Config.min_games_to_replace_agents / len(agents)) or (len(scores) >= Config.min_games_to_replace_agents and sum(scores) >= Config.minimal_relative_agent_improvement * len(scores) / len(agents)):
            torch.save(agents[-1].state_dict(), Config.model_path.joinpath(str(max(map(int, (*re.findall(r'\d+', ''.join(map(str, Config.model_path.iterdir()))), -1))) + 1) + ".pth"))
            agents.append(Agent(Config.n_players))
            agents[-1].load_state_dict(deepcopy(agents[-1].state_dict()))
            agents[-1].training = True
            scores = deque(maxlen=Config.max_results_held)
        elif len(scores) >= Config.min_games_to_replace_agents:
            print(f'{len(scores)} {sum(scores) / len(scores):.2f}')
        else:
            print(f'{len(scores)} {sum(scores)}/{len(scores)}')
        training_buffer += buffer
        train_agent(agents[-1], training_buffer)


if __name__ == "__main__":
    main()
