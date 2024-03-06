from abc import ABC
from dataclasses import dataclass, astuple
from typing import TYPE_CHECKING

from src.entities.BasicResources import BasicResources
from .Move import Move
from ..entities.AllResources import AllResources

if TYPE_CHECKING:
    from src.Game import Game


@dataclass(slots=True, frozen=True)
class GrabResource(Move, ABC):
    resources: BasicResources

    def __repr__(self):
        return self.resources.__repr__()

    def is_valid(self, game: "Game") -> bool:
        if (
            sum(astuple(game.current_player.resources)) + sum(astuple(self.resources))
            > 10
        ):
            return False
        return not (AllResources(
            game.board.resources.red,
            game.board.resources.green,
            game.board.resources.blue,
            game.board.resources.black,
            game.board.resources.white,
        ) - self.resources).lacks()
