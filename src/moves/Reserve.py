from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.entities.Card import Card
from ..entities.AllResources import AllResources

if TYPE_CHECKING:
    from src.Game import Game
from .Move import Move


@dataclass(slots=True, frozen=True)
class Reserve(Move, ABC):
    tier_index: int

    def reserve_card(self, game: "Game", card: Card):
        current_player = game.current_player
        current_player.reserve.append(card)
        if game.board.resources.gold:
            game.board.resources = AllResources(
                game.board.resources.red,
                game.board.resources.green,
                game.board.resources.blue,
                game.board.resources.black,
                game.board.resources.white,
                game.board.resources.gold - 1
            )
            current_player.resources = AllResources(
                current_player.resources.red,
                current_player.resources.green,
                current_player.resources.blue,
                current_player.resources.black,
                current_player.resources.white,
                current_player.resources.gold + 1
            )

    def _can_take_gold(self, game: "Game"):
        return sum(iter(game.current_player.resources)) < 10
