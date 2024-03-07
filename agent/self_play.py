import numpy as np

from Config import Config
from .Agent import Agent
from .policy import policy
from src.Game import Game


def self_play(agent: Agent) -> list[tuple[np.array, np.array, int]]:
    agent.eval()
    examples = []
    game = Game(n_players=Config.n_players)
    while True:
        pi, action = policy(game, agent, 1, Config.n_simulations)
        action_index = game.all_moves.index(action)
        onehot_encoded_action = np.zeros(Config.n_actions)
        onehot_encoded_action[action_index] = 1
        examples.append((game, onehot_encoded_action, 0))
        game = game.perform(action)
        print(len(game.players[1].cards), game.players[1].points)
        if game.is_terminal():
            result = game.get_results()
            for example in examples:
                player_id = example[0].current_player.id
                example[2] = int(result[player_id] == 1)
                example[0] = example[0].get_state()
            return examples
