from dataclasses import astuple

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySplendor.Game import Game
from PySplendor.processing.moves.GrabResource import GrabResource


class GrabThreeResource(GrabResource):
    def perform(self, game: "Game") -> "Game":
        game.board.resources -= self.resources
        game.current_player.resources += self.resources
        return game

    def is_valid(self, game: "Game") -> bool:
        if (
            sum(astuple(game.current_player.resources)) + sum(astuple(self.resources))
            > 10
        ):
            return False
        return not (game.board.resources - self.resources).lacks()
