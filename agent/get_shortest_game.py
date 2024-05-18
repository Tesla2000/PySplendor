from copy import deepcopy
from typing import Generator, Optional, NamedTuple

import numpy as np
import torch

from agent.Agent import Agent
from agent.services.game_end_checker import GameEndChecker
from src.Game import Game
from src.moves import Move


class GameState(NamedTuple):
    game: Game
    move: Optional[Move]


GameSequence = list[GameState]


@torch.no_grad()
def get_shortest_game(game_move_pair: GameState, beta: int, game_end_checker: GameEndChecker,
                      agent: Agent) -> Generator[
    GameSequence, None, None]:
    game = game_move_pair[0]
    if game.is_terminal():
        return
    game_state = game.get_state()
    move_probs = agent(torch.tensor(game_state).float()).flatten().numpy()
    move_indexes = np.argsort(move_probs)
    new_games = []
    for move_index in move_indexes:
        move = Game.all_moves[move_index]
        if move.is_valid(game):
            new_game = game.perform(move)
            if game_end_checker.is_end(new_game):
                yield [GameState(game, move)]
            new_games.append(GameState(new_game, move))
            if len(new_games) == beta:
                break
    for new_game in new_games:
        for game_sequence in get_shortest_game(new_game, beta, deepcopy(game_end_checker), agent):
            game_sequence.append(game_move_pair)
            yield game_sequence
