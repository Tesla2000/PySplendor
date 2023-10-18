from dataclasses import astuple, asdict
from itertools import compress

from splendor.processing._Game import _Game
from splendor.processing.moves.GrabResource import GrabResource


class GrabTwoResource(GrabResource):
    def perform(self, game: _Game) -> None:
        game.board.resources -= self.resources
        game.current_player.resources += self.resources

    def is_valid(self, game: _Game) -> bool:
        tuple_resources = astuple(self.resources)
        if sum(astuple(game.current_player.resources)) + sum(tuple_resources) > 10:
            return False
        resource = next(compress(asdict(self.resources).keys(), tuple_resources))
        if getattr(game.board.resources, resource) < 4:
            return False
        return not (game.board.resources - self.resources).lacks()
