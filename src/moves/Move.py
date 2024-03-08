from abc import ABC, abstractmethod
from dataclasses import dataclass, astuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Game import Game


@dataclass(slots=True, frozen=True)
class Move(ABC):
    @abstractmethod
    def perform(self, game: "Game") -> "Game":
        game = game.copy()
        game.is_blocked[game.current_player] = False
        return game

    @abstractmethod
    def is_valid(self, game: "Game") -> bool:
        pass

    def __hash__(self):
        return astuple(self).__hash__()
