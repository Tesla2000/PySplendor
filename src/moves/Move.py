from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Game import Game


class Move(ABC):
    @abstractmethod
    def perform(self, game: "Game") -> "Game":
        game.is_blocked[game.current_player] = False
        return game

    @abstractmethod
    def is_valid(self, game: "Game") -> bool:
        pass
