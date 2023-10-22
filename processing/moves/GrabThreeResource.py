from dataclasses import astuple

from PySplendor.processing._Game import _Game
from PySplendor.processing.moves.GrabResource import GrabResource


class GrabThreeResource(GrabResource):
    def perform(self, game: _Game) -> None:
        game.board.resources -= self.resources
        game.current_player.resources += self.resources

    def is_valid(self, game: _Game) -> bool:
        if (
            sum(astuple(game.current_player.resources)) + sum(astuple(self.resources))
            > 10
        ):
            return False
        return not (game.board.resources - self.resources).lacks()
