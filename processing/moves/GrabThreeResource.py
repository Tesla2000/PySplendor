from dataclasses import astuple

from PySplendor.processing.GamePrototype import GamePrototype
from PySplendor.processing.moves.GrabResource import GrabResource


class GrabThreeResource(GrabResource):
    def perform(self, game: GamePrototype) -> None:
        game.board.resources -= self.resources
        game.current_player.resources += self.resources

    def is_valid(self, game: GamePrototype) -> bool:
        if (
            sum(astuple(game.current_player.resources)) + sum(astuple(self.resources))
            > 10
        ):
            return False
        return not (game.board.resources - self.resources).lacks()
