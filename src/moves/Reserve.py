from abc import ABC
from dataclasses import dataclass, fields

from src.entities.Card import Card
from typing import TYPE_CHECKING

from ..entities.AllResources import AllResources
from ..entities.BasicResources import BasicResources

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
            game.board.resources = AllResources(**dict((field.name, getattr(game.board.resources, field.name)) for field in fields(BasicResources)), gold=game.board.resources.gold - 1)
            current_player.resources = AllResources(**dict((field.name, getattr(game.board.resources, field.name)) for field in fields(BasicResources)), gold=game.board.resources.gold + 1)
