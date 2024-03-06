from collections import Counter
from dataclasses import asdict, dataclass

from src.entities.BasicResources import BasicResources
from src.entities.Card import empty_card
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Game import Game
from .Move import Move


@dataclass(slots=True, frozen=True)
class BuildReserve(Move):
    index: int

    def perform(self, game: "Game") -> "Game":
        game = Move.perform(self, game)
        current_player = game.current_player
        if current_player.resources.lacks():
            raise ValueError()
        card = current_player.reserve.pop(self.index)
        not_produced = BasicResources(
            **(Counter(asdict(card.cost)) - Counter(asdict(current_player.production)))
        )
        if (current_player.resources - not_produced).lacks():
            raise ValueError()
        current_player.resources -= not_produced
        current_player.cards.append(card)
        return game

    def is_valid(self, game: "Game") -> bool:
        current_player = game.current_player
        if current_player.reserve[self.index] == empty_card:
            return False
        card = current_player.reserve[self.index]
        return not (
            current_player.resources + current_player.production - card.cost
        ).lacks()
