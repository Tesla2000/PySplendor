from src.entities.Card import empty_card
from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .Reserve import Reserve


class ReserveTop(Reserve):
    def _perform(self, game: "Game") -> "Game":
        game = Move._perform(self, game)
        tier = game.board.tiers[self.tier_index]
        card = tier.hidden.pop()
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: "Game") -> bool:
        if not self._can_take_gold(game):
            return False
        tier = game.board.tiers[self.tier_index]
        return bool(tier.hidden) and empty_card in game.current_player.reserve
