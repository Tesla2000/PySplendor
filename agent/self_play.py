from collections import deque
from itertools import cycle

import numpy as np

from Config import Config
from .Agent import Agent
from .policy import policy
from src.Game import Game


def self_play(agents: deque[Agent]) -> list[tuple[np.array, np.array, int]]:
    for agent in agents:
        agent.eval()
    states = []
    game = Game(n_players=Config.n_players)
    for agent in cycle(agents):
        pi, action = policy(game, agent, 1, Config.n_simulations)
        action_index = game.all_moves.index(action)
        onehot_encoded_action = np.zeros(Config.n_actions)
        onehot_encoded_action[action_index] = 1
        states.append((game, onehot_encoded_action, 0))
        game = game.perform(action)
        print(len(game.players[1].cards), game.players[1].points)
        if game.is_terminal():
            result = game.get_results()
            return list((state[0].get_state(), state[1], int(result[state[0].current_player.id] == 1)) for state in states)
