from abc import ABC, abstractmethod

from alpha_trainer.classes.AlphaMove import AlphaMove
from PySplendor.processing.GamePrototype import GamePrototype


class Move(AlphaMove, ABC):
    @abstractmethod
    def perform(self, game: GamePrototype) -> GamePrototype:
        pass

    @abstractmethod
    def is_valid(self, game: GamePrototype) -> bool:
        pass
