import torch

from Config import Config
from agent.Agent import Agent
from agent.get_shortest_game import get_shortest_game, GameState
from src.Game import Game
from src.moves import Move

agent = Agent()
agent.load_state_dict(torch.load(Config.model_path.joinpath('speed_game_16000_26.945.pth')))
agent.eval()


def perform_move_ai(game: Game, beta: int = Config.play_beta) -> Game:
    next_states = tuple(game.perform(valid_move) for valid_move in game.get_possible_actions())
    return max(next_states, key=lambda state: (completion_time := get_shortest_game([GameState(state, None)], beta)).get(game.current_player.id, 0) / completion_time.get(game.players[-1].id, 1))


def perform_move(game: Game, move: Move) -> Game:
    game = game.perform(move)
    game = perform_move_ai(game)
    return game
