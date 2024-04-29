from dataclasses import asdict
from itertools import compress

from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .GrabResource import GrabResource


class GrabTwoResource(GrabResource):
    def _perform(self, game: "Game") -> "Game":
        game = Move._perform(self, game)
        game.board.resources -= self.resources
        game.current_player.resources += self.resources
        # if sum(astuple(game.current_player.resources)) > 10:
        #     raise ValueError
        return game

    def is_valid(self, game: "Game") -> bool:
        resource = next(
            compress(("red", "green", "blue", "black", "white"), iter(self.resources))
        )
        if getattr(game.board.resources, resource) < 4:
            return False
        return super().is_valid(game)
