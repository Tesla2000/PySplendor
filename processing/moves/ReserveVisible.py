from PySplendor.data.Card import empty_card
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySplendor.Game import Game
from PySplendor.processing.moves.Reserve import Reserve


class ReserveVisible(Reserve):
    def __init__(self, tier_index: int, index: int):
        super().__init__(tier_index)
        self.index = index

    def perform(self, game: "Game") -> "Game":
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: "Game") -> bool:
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        return game.current_player.reserve.can_add()
