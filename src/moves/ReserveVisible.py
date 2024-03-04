from dataclasses import dataclass

from src.entities.Card import empty_card
from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .Reserve import Reserve


@dataclass(slots=True)
class ReserveVisible(Reserve):
    index: int

    def perform(self, game: "Game") -> "Game":
        Move.perform(self, game)
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: "Game") -> bool:
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        return game.current_player.reserve.can_add()
