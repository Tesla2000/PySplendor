from abc import ABC, abstractmethod
from alpha_trainer.classes.AlphaMove import AlphaMove
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySplendor.Game import Game


class Move(AlphaMove, ABC):
    @abstractmethod
    def perform(self, game: "Game") -> "Game":
        pass

    @abstractmethod
    def is_valid(self, game: "Game") -> bool:
        pass
