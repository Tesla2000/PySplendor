from collections import defaultdict

import numpy as np
from torch import nn

from agent.search import search
from src.Game import Game


def policy(
    game: Game,
    agent: nn.Module,
    c: float,
    n_simulations: int,
):
    N = defaultdict(lambda: defaultdict(int))
    visited = set()
    P = defaultdict(dict)
    Q = defaultdict(dict)
    initial_state = game.get_state()
    all_moves = game.get_possible_actions()
    for _ in range(n_simulations):
        search(game, agent, c, N, visited, P, Q)
    pi = [N[initial_state][a] for a in all_moves]
    return pi, all_moves[np.argmax(pi)]
