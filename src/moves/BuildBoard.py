from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.entities.Card import empty_card
from .Build import Build

if TYPE_CHECKING:
    from src.Game import Game


@dataclass(slots=True, frozen=True)
class BuildBoard(Build):
    tier_index: int
    index: int

    def perform(self, game: "Game") -> "Game":
        game = Build.perform(self, game)
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        return Build._build(game, card)

    def is_valid(self, game: "Game") -> bool:
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        card = tier.visible[self.index]
        current_player = game.current_player
        return not (
            (current_player.resources + current_player.production) - card.cost
        ).lacks()
