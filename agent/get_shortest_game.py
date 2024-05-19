from typing import Generator

import numpy as np
import torch

from agent.Agent import Agent
from agent.entities import GameState, NoValidMove
from agent.services.game_end_checker import GameEndChecker
from src.Game import Game


@torch.no_grad()
def get_shortest_game(raw_game_states: list[GameState], beta: int, game_end_checker: GameEndChecker,
                      agent: Agent) -> Generator[GameState, None, int]:
    game_states = list(filter(lambda game_state: not game_state.game.is_terminal(), raw_game_states))
    if not game_states:
        print("No valid moves")
        raise NoValidMove(raw_game_states)
    board_states = tuple(game.get_state() for game, _, _ in game_states)
    move_probs = agent(torch.tensor(board_states).float()).flatten().numpy()
    move_indexes = np.argsort(move_probs)
    new_games = []
    for move_index in move_indexes:
        game_index, move_index = divmod(move_index, Game.action_size)
        game_state = game_states[game_index]
        move = Game.all_moves[move_index]
        if move.is_valid(game_state.game):
            new_game = game_state.game.perform(move)
            new_state = GameState(new_game, move, game_state)
            if game_end_checker.is_end(new_game):
                yield new_state
            new_games.append(new_state)
            if len(new_games) == beta:
                break
    yield from get_shortest_game(new_games, beta, game_end_checker, agent)
