import random
from collections import deque
from itertools import count

import numpy as np
from tqdm import tqdm

from Config import Config
from src.Game import Game
from .Agent import Agent
from .policy import policy


def self_play(
    agents: deque[Agent],
) -> tuple[list[tuple[np.array, np.array, int]], list[Agent]]:
    states = []
    winners = []
    game = Game(n_players=Config.n_players)
    for agent in agents:
        agent.eval()
    id_to_agent = dict(
        (player.id, agent)
        for agent, player in zip(random.sample(agents, Config.n_players), game.players)
    )
    results, winner = _perform_game(game, [], id_to_agent)
    states += results
    winners.append(winner)
    return states, winners


def _perform_game(
    game: Game, states: list, id_to_agent: dict[int, Agent]
) -> tuple[list[tuple[np.array, np.array, int]], Agent]:
    for turn in tqdm(count()):
        agent = id_to_agent[game.current_player.id]
        pi, action = policy(game, agent, Config.c, Config.n_simulations)
        action_index = game.all_moves.index(action)
        onehot_encoded_action = np.zeros(Config.n_actions)
        onehot_encoded_action[action_index] = 1
        states.append((game, action, 0))
        game = game.perform(action)
        if game.is_terminal():
            result = game.get_results()
            return (
                list(
                    (
                        state[0].get_state(),
                        np.eye(Config.n_actions)[game.all_moves.index(state[1])],
                        int(result[state[0].current_player.id] == 1),
                    )
                    for state in states
                    if state[1] != game.null_move
                ),
                id_to_agent[
                    next(player.id for player in game.players if result[player.id])
                ],
            )
