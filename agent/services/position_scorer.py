from abc import ABC, abstractmethod
from functools import partial

from agent.entities import GameMovePairs
from utils.get_not_finished_moves import get_not_finished_moves


class PositionScorer(ABC):
    @abstractmethod
    def score(self, game_move_pairs: GameMovePairs, other_player_id: int, current_player_id: int) -> float:
        pass


class RelativeScorer(PositionScorer):
    def score(self, game_move_pairs: GameMovePairs, other_player_id: int, current_player_id: int) -> float:
        game_completion_times = dict(map(partial(get_moves_taken_to_complete, game_move_pairs=game_move_pairs),
                                         (current_player_id, other_player_id)))
        return game_completion_times[other_player_id] / game_completion_times[current_player_id]


class AbsoluteScorer(PositionScorer):
    def score(self, game_move_pairs: GameMovePairs, other_player_id: int, current_player_id: int) -> float:
        return -get_moves_taken_to_complete(current_player_id, game_move_pairs)[-1]


def get_moves_taken_to_complete(player_id: int, game_move_pairs: GameMovePairs) -> tuple[int, int]:
    removed_finished_games = get_not_finished_moves(player_id, game_move_pairs)
    return player_id, sum(1 for _ in removed_finished_games) + int(
        player_id == game_move_pairs[0].game.current_player.id)
