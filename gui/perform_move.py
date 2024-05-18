from itertools import dropwhile

import torch

from Config import Config
from agent.Agent import Agent
from agent.entities import GameMovePairs, NoValidMove
from agent.get_shortest_games import get_shortest_games
from agent.services.game_end_checker import EndOnSecondPlayer
from src.Game import Game
from src.entities.BasicResources import BasicResources
from src.moves import Move, GrabTwoResource

agent = Agent()
agent.load_state_dict(torch.load(Config.model_path.joinpath('speed_game_16000_26.945.pth')))
agent.eval()


def perform_move_ai(game: Game, beta: int = Config.play_beta) -> Game:
    def _simulate_and_score_game(state: Game) -> float:
        game_end_checker = EndOnSecondPlayer()
        try:
            shortest_games = get_shortest_games(state, game_end_checker, beta, agent)
        except NoValidMove as e:
            return 1 + (1 if e.blocked_player != game.current_player.id else -1) / 1000
        return min(_score_game(shortest_game, game.players[-1].id, game.current_player.id) for shortest_game in
                   shortest_games)

    return max(map(game.perform, game.get_possible_actions()), key=_simulate_and_score_game)


def perform_move(game: Game, move: Move) -> Game:
    game = game.perform(move)
    game = perform_move_ai(game)
    return game


def _score_game(shortest_game: GameMovePairs, other_player_id: int, current_player_id: int) -> float:
    def _get_moved_taken_to_complete(player_id: int) -> tuple[int, int]:
        games_belonging_to_player = tuple(filter(
            lambda game_state: game_state.game.current_player.id == player_id and game_state.move, shortest_game))
        removed_finished_games = tuple(dropwhile(
            lambda game_state: game_state.game.current_player.points >= Config.min_n_points_to_finish,
            games_belonging_to_player))
        return player_id, sum(1 for _ in removed_finished_games) + int(
            player_id == shortest_game[0].game.current_player.id)

    game_completion_times = dict(map(_get_moved_taken_to_complete, (current_player_id, other_player_id)))
    return game_completion_times[other_player_id] / game_completion_times[current_player_id]


if __name__ == '__main__':
    game = Game()
    perform_move(game, GrabTwoResource(BasicResources(black=2)))
