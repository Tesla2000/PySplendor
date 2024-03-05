from collections import defaultdict
from math import sqrt

from torch import nn, Tensor

from Config import Config
from src.Game import Game
from .Agent import Agent


def train_agent():
    agent = Agent(Config.n_players)
    agent.eval()
    examples = []
    examples_per_game = []
    for i in range(Config.n_games):
        N = defaultdict(dict)
        game = Game(n_players=Config.n_players)
        while True:
            pi = policy(game, agent, 1, Config.n_simulations, N)
            examples_per_game.append((game, pi, 0))
            game = game.perform(pi)
            if game.is_terminal():
                for example in examples_per_game:
                    example[2] = game.get_state()
                break
        examples += examples_per_game
    return examples


def search(game: Game, agent: nn.Module, c: float, N: defaultdict, visited: set = None):
    if visited is None:
        visited = set()
    P, Q = defaultdict(dict), defaultdict(dict)
    state = game.get_state()
    if game.is_terminal():
        return game.get_results()
    if state not in visited:
        visited.add(state)
        P[state], v = agent(state)
        return -v

    max_u, best_a = -float("inf"),  None
    for action in game.get_possible_actions():
        u = Q[state][action] + c * P[state][action] * sqrt(sum(N[state])) / (1 + N[state][action])
        if u > max_u:
            max_u = u
            best_a = action
    action = best_a

    next_game_state = game.perform(action)
    v = search(next_game_state, agent, c, N, visited)

    Q[state][action] = (N[state][action] * Q[state][action] + v) / (N[state][action] + 1)
    N[state][action] += 1
    return -v


def policy(game: Game, agent: nn.Module, c: float, n_simulations: int, N: defaultdict):
    visited = set()
    for i in range(n_simulations):
        search(game, agent, c, N, visited)
    return [N[game.get_state()][a] for a in game.get_possible_actions()]
