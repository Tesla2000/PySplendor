from collections import deque
from itertools import count, cycle, islice
from more_itertools import windowed

import numpy as np
from tqdm import tqdm

from Config import Config
from .Agent import Agent
from .policy import policy
from src.Game import Game


def self_play(
    agents: deque[Agent],
) -> tuple[list[tuple[np.array, np.array, int]], list[Agent]]:
    states = []
    winners = []
    initial_state = Game(n_players=Config.n_players)
    for agent in agents:
        agent.eval()
    for agents_in_order in islice(
        windowed(cycle(agents), Config.n_players), Config.n_players
    ):
        game = initial_state.copy()
        id_to_agent = dict(
            (player.id, agent) for agent, player in zip(agents_in_order, game.players)
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
                        (onehot_encoded_action := np.zeros(Config.n_actions), onehot_encoded_action.__setitem__(game.all_moves.index(state[1]), 1))[0],
                        int(result[state[0].current_player.id] == 1),
                    )
                    for state in states
                ),
                id_to_agent[
                    next(player.id for player in game.players if result[player.id])
                ],
            )
