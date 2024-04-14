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
    N = defaultdict(list)
    visited = set()
    P = defaultdict(list)
    Q = defaultdict(list)
    initial_state = game.get_state()
    all_moves = game.get_possible_actions()
    for _ in range(n_simulations):
        search(game.copy(), agent, c, N, visited, P, Q)
    pi = np.array([N[initial_state][a] for a in all_moves])
    return pi, all_moves[np.argmax(pi)]
