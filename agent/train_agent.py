from collections import defaultdict
from dataclasses import astuple
from math import sqrt

from torch import nn, Tensor

from Config import Config
from src.Game import Game
from src.entities.Player import Player
from .Agent import Agent


def train_agent():
    agent = Agent(Config.n_players)
    agent.eval()
    examples = []
    examples_per_game = []
    for i in range(Config.n_games):
        N = defaultdict(lambda: defaultdict(int))
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


def search(game: Game, agent: nn.Module, c: float, N: defaultdict, visited: set, P: defaultdict, Q: defaultdict, evaluated_player: Player = None):
    if evaluated_player is None:
        evaluated_player = game.current_player
    state = game.get_state()
    if game.is_terminal():
        return game.get_results()[evaluated_player]
    if state not in visited:
        visited.add(state)
        move_scores, v = agent(Tensor([state]))
        for index, move in enumerate(game.all_moves):
            P[state][move] = move_scores[0, index]
        return -v

    max_u, best_a = -float("inf"),  None
    for action in game.get_possible_actions():
        u = Q[state].get(action, 1) + c * P[state][action] * sqrt(sum(N[state].values())) / (1 + N[state][action])
        if u > max_u:
            max_u = u
            best_a = action
    action = best_a

    next_game_state = game.perform(action)
    v = search(next_game_state, agent, c, N, visited, P, Q, evaluated_player)

    Q[state][action] = (N[state][action] * Q[state].get(action, 1) + v) / (N[state][action] + 1)
    N[state][action] += 1
    return -v


def policy(game: Game, agent: nn.Module, c: float, n_simulations: int, N: defaultdict):
    visited = set()
    P = defaultdict(dict)
    Q = defaultdict(dict)
    initial_state = game.get_state()
    all_moves = game.get_possible_actions()
    for i in range(n_simulations):
        search(game, agent, c, N, visited, P, Q)
    return [N[initial_state][astuple(a)] for a in all_moves]
