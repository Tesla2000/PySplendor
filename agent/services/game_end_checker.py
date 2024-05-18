from abc import ABC, abstractmethod
from operator import attrgetter

from Config import Config
from src.Game import Game


class GameEndChecker(ABC):
    @abstractmethod
    def is_end(self, game: Game) -> bool:
        pass


class EndOnFirstPlayer(GameEndChecker):
    def is_end(self, game: Game) -> bool:
        return any(map(Config.min_n_points_to_finish.__le__, map(attrgetter("points"), game.players)))


class EndOnSecondPlayer(GameEndChecker):
    def is_end(self, game: Game) -> bool:
        return all(player.points >= Config.min_n_points_to_finish for player in game.players)
