from src.entities.Card import empty_card
from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .Reserve import Reserve


class ReserveTop(Reserve):
    def perform(self, game: "Game") -> "Game":
        Move.perform(self, game)
        tier = game.board.tiers[self.tier_index]
        card = tier.hidden.pop()
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: "Game") -> bool:
        tier = game.board.tiers[self.tier_index]
        return bool(tier.hidden) and empty_card in game.current_player.reserve
