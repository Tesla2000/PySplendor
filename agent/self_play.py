import random
from collections import deque
from itertools import count

import numpy as np
from numpy import argmax
from tqdm import tqdm

from Config import Config
from src.Game import Game
from .Agent import Agent
from .MCTS import MCTS


def self_play(
    agents: deque[Agent],
) -> tuple[list[tuple[np.array, np.array, int]], list[Agent]]:
    states = []
    winners = []
    game = Game(n_players=Config.n_players)
    for agent in agents:
        agent.eval()
    id_to_agent = dict(
        (player.id, MCTS(game, agent))
        for agent, player in zip(random.sample(agents, Config.n_players), game.players)
    )
    results, winner = _perform_game(game, [], id_to_agent)
    states += results
    winners.append(winner)
    return states, winners


def _perform_game(
    game: Game, states: list, id_to_mcts: dict[int, MCTS]
) -> tuple[list[tuple[np.array, np.array, int]], MCTS]:
    for _ in tqdm(count()):
        mcts = id_to_mcts[game.current_player.id]
        mcts_probs = mcts.search(game.get_state())
        states.append((game, mcts_probs, 0))
        action = game.all_moves[argmax(mcts_probs)]
        game = game.perform(action)
        if game.is_terminal():
            result = game.get_results()
            return (
                list(
                    (
                        state[0].get_state(),
                        state[1],
                        int(result[state[0].current_player.id] == 1),
                    )
                    for state in states
                ),
                id_to_mcts[
                    next(player.id for player in game.players if result[player.id])
                ],
            )
