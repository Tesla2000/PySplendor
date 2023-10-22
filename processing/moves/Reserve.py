from abc import ABC

from PySplendor.data.Card import Card
from PySplendor.processing._Game import _Game
from PySplendor.processing.moves.Move import Move


class Reserve(Move, ABC):
    def __init__(self, tier_index: int):
        self.tier_index = tier_index

    def reserve_card(self, game: _Game, card: Card):
        current_player = game.current_player
        current_player.reserve.append(card)
        if game.board.resources.gold:
            game.board.resources.gold -= 1
            current_player.resources.gold += 1
