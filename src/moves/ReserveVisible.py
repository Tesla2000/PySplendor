from dataclasses import dataclass

from src.entities.Card import empty_card
from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game
from .Reserve import Reserve


@dataclass(slots=True, frozen=True)
class ReserveVisible(Reserve):
    index: int

    def _perform(self, game: "Game") -> "Game":
        game = Move._perform(self, game)
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        self.reserve_card(game, card)
        return game

    def is_valid(self, game: "Game") -> bool:
        if not self._can_take_gold(game):
            return False
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        return game.current_player.reserve.can_add()
