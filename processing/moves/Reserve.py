from abc import ABC

from PySplendor.data.Card import Card
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySplendor.Game import Game
from PySplendor.processing.moves.Move import Move


class Reserve(Move, ABC):
    def __init__(self, tier_index: int):
        self.tier_index = tier_index

    def reserve_card(self, game: "Game", card: Card):
        current_player = game.current_player
        current_player.reserve.append(card)
        if game.board.resources.gold:
            game.board.resources.gold -= 1
            current_player.resources.gold += 1
