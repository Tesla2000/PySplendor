from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from alpha_trainer.src.alpha_trainer import AlphaMove

if TYPE_CHECKING:
    from PySplendor.Game import Game


class Move(AlphaMove, ABC):
    @abstractmethod
    def perform(self, game: "Game") -> "Game":
        pass

    @abstractmethod
    def is_valid(self, game: "Game") -> bool:
        pass
