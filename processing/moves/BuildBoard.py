from collections import Counter
from dataclasses import asdict

from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.Card import empty_card
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySplendor.Game import Game
from PySplendor.processing.moves.Move import Move


class BuildBoard(Move):
    def __init__(self, tier_index: int, index: int):
        self.tier_index = tier_index
        self.index = index

    def perform(self, game: "Game") -> "Game":
        current_player = game.current_player
        if current_player.resources.lacks():
            raise ValueError()
        tier = game.board.tiers[self.tier_index]
        card = tier.pop(self.index)
        not_produced = BasicResources(
            **(Counter(asdict(card.cost)) - Counter(asdict(current_player.production)))
        )
        if (current_player.resources - not_produced).lacks():
            raise ValueError()
        current_player.resources -= not_produced
        current_player.cards.append(card)
        return game

    def is_valid(self, game: "Game") -> bool:
        tier = game.board.tiers[self.tier_index]
        if tier.visible[self.index] == empty_card:
            return False
        card = tier.visible[self.index]
        current_player = game.current_player
        return not (
            current_player.resources + current_player.production - card.cost
        ).lacks()
