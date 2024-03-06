from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.entities.Card import Card
from ..entities.AllResources import AllResources

if TYPE_CHECKING:
    from src.Game import Game
from .Move import Move


@dataclass(slots=True, frozen=True)
class Build(Move, ABC):
    @staticmethod
    def _build(game: "Game", card: Card) -> "Game":
        current_player = game.current_player
        gold_paid_for_red = max(0, card.cost.red - current_player.production.red - current_player.resources.red)
        gold_paid_for_green = max(0, card.cost.green - current_player.production.green - current_player.resources.green)
        gold_paid_for_blue = max(0, card.cost.blue - current_player.production.blue - current_player.resources.blue)
        gold_paid_for_black = max(0, card.cost.black - current_player.production.black - current_player.resources.black)
        gold_paid_for_white = max(0, card.cost.white - current_player.production.white - current_player.resources.white)
        cost = AllResources(
            max(0, card.cost.red - current_player.production.red - gold_paid_for_red),
            max(0, card.cost.green - current_player.production.green - gold_paid_for_green),
            max(0, card.cost.blue - current_player.production.blue - gold_paid_for_blue),
            max(0, card.cost.black - current_player.production.black - gold_paid_for_black),
            max(0, card.cost.white - current_player.production.white - gold_paid_for_white),
            sum((gold_paid_for_red, gold_paid_for_green, gold_paid_for_blue, gold_paid_for_black, gold_paid_for_white)),
        )
        current_player.resources = AllResources(
            max(0, current_player.resources.red - cost.red),
            max(0, current_player.resources.green - cost.green),
            max(0, current_player.resources.blue - cost.blue),
            max(0, current_player.resources.black - cost.black),
            max(0, current_player.resources.white - cost.white),
            current_player.resources.gold - cost.gold,
        )
        game.board.resources = AllResources(
            game.board.resources.red + cost.red,
            game.board.resources.green + cost.green,
            game.board.resources.blue + cost.blue,
            game.board.resources.black + cost.black,
            game.board.resources.white + cost.white,
            game.board.resources.gold + cost.gold,
        )
        current_player.cards.append(card)
        return game
