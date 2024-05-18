from copy import deepcopy
from typing import Generator, Optional, NamedTuple

import numpy as np
import torch

from agent.Agent import Agent
from agent.services.game_end_checker import GameEndChecker
from src.Game import Game
from src.moves import Move


class GameMovePair(NamedTuple):
    game: Game
    move: Move


GameMovePairs = list[GameMovePair]


class GameState(NamedTuple):
    game: Game
    move: Optional[Move] = None
    previous_state: Optional["GameState"] = None

    def to_list(self) -> GameMovePairs:
        output = [GameMovePair(self.previous_state.game, self.move)]
        prev_state = self.previous_state
        while prev_state.previous_state:
            output.append(GameMovePair(prev_state.previous_state.game, prev_state.move))
            prev_state = prev_state.previous_state
        return output


@torch.no_grad()
def get_shortest_game(game_states: list[GameState], beta: int, game_end_checker: GameEndChecker,
                      agent: Agent) -> Generator[GameState, None, None]:
    game_states = list(filter(lambda game_state: not game_state.game.is_terminal(), game_states))
    if not game_states:
        print("No valid moves")
        return
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
    yield from get_shortest_game(new_games, beta, deepcopy(game_end_checker), agent)
