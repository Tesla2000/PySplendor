from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.entities.Card import empty_card
from .Build import Build

if TYPE_CHECKING:
    from src.Game import Game


@dataclass(slots=True, frozen=True)
class BuildReserve(Build):
    index: int

    def perform(self, game: "Game") -> "Game":
        game = Build.perform(self, game)
        current_player = game.current_player
        card = current_player.reserve.pop(self.index)
        return Build._build(game, card)

    def is_valid(self, game: "Game") -> bool:
        current_player = game.current_player
        if current_player.reserve[self.index] == empty_card:
            return False
        card = current_player.reserve[self.index]
        return not (
            current_player.resources + current_player.production - card.cost
        ).lacks()
