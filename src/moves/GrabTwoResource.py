from dataclasses import astuple, asdict
from itertools import compress

from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .GrabResource import GrabResource


class GrabTwoResource(GrabResource):
    def perform(self, game: "Game") -> "Game":
        Move.perform(self, game)
        game.board.resources -= self.resources
        game.current_player.resources += self.resources
        return game

    def is_valid(self, game: "Game") -> bool:
        tuple_resources = astuple(self.resources)
        if sum(astuple(game.current_player.resources)) + sum(tuple_resources) > 10:
            return False
        resource = next(compress(asdict(self.resources).keys(), tuple_resources))
        if getattr(game.board.resources, resource) < 4:
            return False
        return not (game.board.resources - self.resources).lacks()
