import re
from collections import deque, defaultdict
from copy import deepcopy
from itertools import count

import torch

from Config import Config
from agent.Agent import Agent
from agent.self_play import self_play
from agent.train_agent import train_agent


def main():
    training_buffer = deque(maxlen=Config.training_buffer_len)
    agents = deque((Agent(Config.n_players) for _ in range(Config.n_players)), maxlen=Config.n_players)
    agent_scores = defaultdict(int, ((id(agent), 0) for agent in agents))
    for _ in (count() if Config.n_games is None else range(Config.n_games)):
        buffer, agent = self_play(agents)
        agent_scores[id(agent)] += 1
        if sum(agent_scores.values()) >= Config.min_games_to_replace_agents and agent_scores[id(agents[-1])] > Config.minimal_relative_agent_improvement * sum(agent_scores.values()) / len(agents):
            torch.save(agent[-1].state_dict(), Config.model_path.joinpath(str(max(map(int, (*re.findall(r'\d+', ''.join(Config.model_path.iterdir())), -1))) + 1) + ".pth"))
            agents.append(Agent(Config.n_players).load_state_dict(deepcopy(agent[-1].state_dict())))
            agents[-1].trained = True
            agent_scores = defaultdict(int, ((id(agent), 0) for agent in agents))
        print(agent_scores[id(agents[-1])], sum(agent_scores.values()), agent_scores[id(agents[-1])] / sum(agent_scores.values()))
        training_buffer += buffer
        train_agent(agents[-1], training_buffer)


if __name__ == "__main__":
    main()
