from dataclasses import astuple

from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .GrabResource import GrabResource


class GrabThreeResource(GrabResource):
    def perform(self, game: "Game") -> "Game":
        game = Move.perform(self, game)
        game.board.resources -= self.resources
        game.current_player.resources += self.resources
        if sum(astuple(game.current_player.resources)) > 10:
            raise ValueError
        return game

    def is_valid(self, game: "Game") -> bool:
        if (
            sum(astuple(game.current_player.resources)) + sum(astuple(self.resources))
            > 10
        ):
            return False
        return not (game.board.resources - self.resources).lacks()
