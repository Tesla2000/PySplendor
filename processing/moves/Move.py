from abc import ABC, abstractmethod

from alpha_trainer.classes.AlphaMove import AlphaMove
from splendor.processing._Game import _Game


class Move(AlphaMove, ABC):
    @abstractmethod
    def perform(self, game: _Game) -> None:
        pass

    @abstractmethod
    def is_valid(self, game: _Game) -> bool:
        pass
