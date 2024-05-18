from typing import NamedTuple, Optional

from src.Game import Game
from src.moves import Move


class GameMovePair(NamedTuple):
    game: Game
    move: Move


class NoValidMove(ValueError):
    blocked_player: int

    def __init__(self, blocked_player: int):
        self.blocked_player = blocked_player


GameMovePairs = list[GameMovePair]


class GameState(NamedTuple):
    game: Game
    move: Optional[Move] = None
    previous_state: Optional["GameState"] = None

    def to_list(self) -> GameMovePairs:
        output = [GameMovePair(self.previous_state.game, self.move)]
        prev_state = self.previous_state
        while prev_state.previous_state:
            output.append(GameMovePair(prev_state.previous_state.game, prev_state.move))
            prev_state = prev_state.previous_state
        return output