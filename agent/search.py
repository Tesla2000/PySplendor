from math import sqrt
from collections import defaultdict

import torch
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
        return -game.get_results()[game.current_player.id]
    state = game.get_state()
    if state not in visited:
        visited.add(state)
        with torch.no_grad():
            move_scores, v = agent(Tensor([state]))
        tuple(
            P[state].__setitem__(move, move_scores[0, index].item())
            for index, move in enumerate(game.all_moves)
        )
        return -v.item()
    q_state = Q[state]
    p_state = P[state]
    n_state = N[state]
    sqrt_value = sqrt(sum(n_state.values()))

    # def _get_action(game: Game):
    #     return max(
    #         game.get_possible_actions(),
    #         key=lambda action: q_state.get(action, 1) + c * p_state[action] * sqrt_value / (1 + n_state[action]),
    #     )
    # def _get_action(game: Game):
    #     best_action = None
    #     best_value = -float('inf')
    #     for action in game.all_moves:
    #         value = q_state.get(action, 1) + c * p_state[action] * sqrt_value / (1 + n_state[action])
    #         if value > best_value and action.is_valid(game):
    #             best_value, best_action = value, action
    #     return best_action
    action = max(
        game.get_possible_actions(),
        key=lambda action: q_state.get(action, 1) + c * p_state[action] * sqrt_value / (1 + n_state[action]),
    )
    next_game_state = game.perform(action)
    v = search(next_game_state, agent, c, N, visited, P, Q)

    Q[state][action] = (N[state][action] * Q[state].get(action, 1) + v) / (
        N[state][action] + 1
    )
    N[state][action] += 1
    return -v
