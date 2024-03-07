from collections import deque
from itertools import cycle

import numpy as np
from tqdm import tqdm

from Config import Config
from .Agent import Agent
from .policy import policy
from src.Game import Game


def self_play(agents: deque[Agent]) -> tuple[list[tuple[np.array, np.array, int]], Agent]:
    states = []
    game = Game(n_players=Config.n_players)
    id_to_agent = dict((player.id, agent) for agent, player in zip(agents, game.players))
    for agent in agents:
        agent.eval()
    for agent in tqdm(cycle(agents)):
        pi, action = policy(game, agent, 1, Config.n_simulations)
        action_index = game.all_moves.index(action)
        onehot_encoded_action = np.zeros(Config.n_actions)
        onehot_encoded_action[action_index] = 1
        states.append((game, onehot_encoded_action, 0))
        game = game.perform(action)
        if game.is_terminal():
            result = game.get_results()
            return (list((state[0].get_state(), state[1], int(result[state[0].current_player.id] == 1)) for state in states),
                    id_to_agent[next(player.id for player in game.players if result[player.id])])
