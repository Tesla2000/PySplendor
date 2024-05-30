import sys
from abc import ABC, abstractmethod

import numpy as np
import torch

from Config import Config
from agent.Agent import Agent
from agent.entities import GameState, NoValidMove
from agent.get_shortest_games import get_shortest_games
from agent.services.game_end_checker import EndOnSecondPlayer
from agent.services.position_scorer import AbsoluteScorer
from src.Game import Game
from utils.get_not_finished_moves import get_not_finished_moves

agent = Agent()
agent.load_state_dict(torch.load(Config.ai_weights))
agent.eval()
position_scorer = AbsoluteScorer()


class AiMoveService(ABC):
    @abstractmethod
    def perform_move(self, game: Game):
        pass


class AiMoveDifferential(AiMoveService):
    def perform_move(self, game: Game) -> Game:
        beta: int = Config.play_beta

        def simulate_and_score_game(state: Game) -> float:
            def min_moves(game_state: GameState) -> int:
                game_state = game_state.to_list()
                players = game_state[0].game.players
                winners = tuple(
                    filter(
                        lambda
                            player: player.id >= Config.min_n_points_to_finish,
                        players
                    )
                )
                if not winners:
                    return sys.maxsize
                winner = winners[0]
                if winner.id != game.current_player.id:
                    return sys.maxsize
                return sum(1 for _ in
                           get_not_finished_moves(winner.id, game_state))

            game_end_checker = EndOnSecondPlayer()
            try:
                shortest_games = get_shortest_games(state,
                                                    game_end_checker, beta,
                                                    agent)
            except NoValidMove as e:
                return -min(map(min_moves, e.raw_game_states))
            return min(
                position_scorer.score(shortest_game, game.players[-1].id,
                                      game.current_player.id) for
                shortest_game in
                shortest_games)

        return max(map(game.perform, game.get_possible_actions()),
                   key=simulate_and_score_game)


class VeryEasyAI(AiMoveService):
    def perform_move(self, game: Game) -> Game:
        state = game.get_state()
        output = agent(torch.Tensor(state))
        move_indexes = np.argsort(output)
        for move_index in move_indexes:
            move = game.all_moves[move_index]
            if move.is_valid(game):
                return game.perform(move)

