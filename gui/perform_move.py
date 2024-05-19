import sys

import torch

from Config import Config
from agent.Agent import Agent
from agent.entities import NoValidMove, GameState
from agent.get_shortest_games import get_shortest_games
from agent.services.game_end_checker import EndOnSecondPlayer
from agent.services.position_scorer import AbsoluteScorer
from src.Game import Game
from src.entities.BasicResources import BasicResources
from src.moves import Move, GrabTwoResource
from utils.get_not_finished_moves import get_not_finished_moves

agent = Agent()
agent.load_state_dict(torch.load(Config.ai_weights))
agent.eval()
position_scorer = AbsoluteScorer()


def perform_move_ai(game: Game, beta: int = Config.play_beta) -> Game:
    def simulate_and_score_game(state: Game) -> float:
        def min_moves(game_state: GameState) -> int:
            game_state = game_state.to_list()
            players = game_state[0].game.players
            winners = tuple(filter(lambda player: player.id >= Config.min_n_points_to_finish, players))
            if not winners:
                return sys.maxsize
            winner = winners[0]
            if winner.id != game.current_player.id:
                return sys.maxsize
            return sum(1 for _ in get_not_finished_moves(winner.id, game_state))

        game_end_checker = EndOnSecondPlayer()
        try:
            shortest_games = get_shortest_games(state, game_end_checker, beta, agent)
        except NoValidMove as e:
            return -min(map(min_moves, e.raw_game_states))
        return min(
            position_scorer.score(shortest_game, game.players[-1].id, game.current_player.id) for shortest_game in
            shortest_games)

    return max(map(game.perform, game.get_possible_actions()), key=simulate_and_score_game)


def perform_move(game: Game, move: Move) -> Game:
    game = game.perform(move)
    game = perform_move_ai(game)
    print("performed move AI")
    return game


if __name__ == '__main__':
    game = Game()
    perform_move(game, GrabTwoResource(BasicResources(black=2)))
