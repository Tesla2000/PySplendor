from typing import TYPE_CHECKING

from .GrabResource import GrabResource
from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game


class GrabThreeResource(GrabResource):
    def _perform(self, game: "Game") -> "Game":
        game = Move._perform(self, game)
        game.board.resources -= self.resources
        game.current_player.resources += self.resources
        # if sum(astuple(game.current_player.resources)) > 10:
        #     raise ValueError
        return game
