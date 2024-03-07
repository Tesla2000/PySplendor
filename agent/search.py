from collections import defaultdict
from math import sqrt

from torch import nn, Tensor

from src.Game import Game


def search(
    game: Game,
    agent: nn.Module,
    c: float,
    N: defaultdict,
    visited: set,
    P: defaultdict,
    Q: defaultdict,
):
    if game.is_terminal():
        return game.get_results()[game.current_player.id]
    state = game.get_state()
    if state not in visited:
        visited.add(state)
        move_scores, v = agent(Tensor([state]))
        tuple(
            P[state].__setitem__(move, move_scores[0, index])
            for index, move in enumerate(game.all_moves)
        )
        return -v

    action = max(
        game.get_possible_actions(),
        key=lambda action: Q[state].get(action, 1)
        + c * P[state][action] * sqrt(sum(N[state].values())) / (1 + N[state][action]),
    )

    next_game_state = game.perform(action)
    v = search(next_game_state, agent, c, N, visited, P, Q)

    Q[state][action] = (N[state][action] * Q[state].get(action, 1) + v) / (
        N[state][action] + 1
    )
    N[state][action] += 1
    return -v