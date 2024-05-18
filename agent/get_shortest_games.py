import sys

from agent.Agent import Agent
from agent.entities import GameMovePairs
from agent.get_shortest_game import get_shortest_game, GameState
from agent.services.game_end_checker import GameEndChecker
from src.Game import Game


def get_shortest_games(root: Game, game_end_checker: GameEndChecker, beta: int, agent: Agent) -> list[GameMovePairs]:
    shortest_game_length = sys.maxsize
    shortest_games = []
    for shortest_game in get_shortest_game([GameState(root, None)], beta, game_end_checker, agent):
        shortest_game = shortest_game.to_list()
        if len(shortest_game) <= shortest_game_length:
            shortest_game_length = len(shortest_game)
        else:
            break
        shortest_games.append(shortest_game)
    if shortest_games:
        return shortest_games
