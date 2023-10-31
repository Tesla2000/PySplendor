from PySplendor.data.Card import empty_card
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySplendor.Game import Game
from PySplendor.processing.moves.Reserve import Reserve


class ReserveTop(Reserve):
    def perform(self, game: "Game") -> "Game":
        tier = game.board.tiers[self.tier_index]
        card = tier.hidden.pop()
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: "Game") -> bool:
        tier = game.board.tiers[self.tier_index]
        return bool(tier.hidden) and empty_card in game.current_player.reserve
