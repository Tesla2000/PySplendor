from dataclasses import dataclass
from typing import TYPE_CHECKING

from .Move import Move

if TYPE_CHECKING:
    from src.Game import Game

@dataclass(slots=True, frozen=True)
class NullMove(Move):
    def perform(self, game: "Game") -> "Game":
        game.is_blocked[game.current_player] = True
        return game

    def is_valid(self, game: "Game") -> bool:
        return not all(game.is_blocked.values())
