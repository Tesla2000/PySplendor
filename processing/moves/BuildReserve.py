from collections import Counter
from dataclasses import asdict

from splendor.data.BasicResources import BasicResources
from splendor.data.Card import empty_card
from splendor.processing._Game import _Game
from splendor.processing.moves.Move import Move


class BuildReserve(Move):
    def __init__(self, index: int):
        self.index = index

    def perform(self, game: _Game) -> None:
        current_player = game.current_player
        card = current_player.reserve.pop(self.index)
        not_produced = BasicResources(
            **(Counter(asdict(card.cost)) - Counter(asdict(current_player.production)))
        )
        current_player.resources -= not_produced
        current_player.cards.append(card)

    def is_valid(self, game: _Game) -> bool:
        current_player = game.current_player
        if current_player.reserve[self.index] == empty_card:
            return False
        card = current_player.reserve[self.index]
        return not (
            current_player.resources + current_player.production - card.cost
        ).lacks()
