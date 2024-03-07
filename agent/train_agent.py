from collections import defaultdict
from math import sqrt

import numpy as np
from torch import nn, Tensor
from tqdm import tqdm

from Config import Config
from src.Game import Game
from .Agent import Agent


def train_agent():
    agent = Agent(Config.n_players)
    agent.eval()
    examples = []
    examples_per_game = []
    for i in range(Config.n_games):
        game = Game(n_players=Config.n_players)
        while True:
            pi, action = policy(game, agent, 1, Config.n_simulations)
            examples_per_game.append((game, pi, 0))
            game = game.perform(action)
            print(len(game.players[1].cards), game.players[1].points)
            if game.is_terminal():
                result = game.get_results()
                for example in examples_per_game:
                    player_id = example[0].current_player.id
                    example[2] = result[player_id]
                break
        examples += examples_per_game
        break
    return examples


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
    for _ in tqdm(range(n_simulations)):
        search(game, agent, c, N, visited, P, Q)
    pi = [N[initial_state][a] for a in all_moves]
    return pi, all_moves[np.argmax(pi)]
