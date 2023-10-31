from dataclasses import dataclass
from typing import Generator

from PySplendor.data.Board import Board
from PySplendor.data.Player import Player
from alpha_trainer.classes.AlphaGameResult import AlphaGameResult
from alpha_trainer.classes.AlphaMove import AlphaMove
from alpha_trainer.classes.AlphaPlayer import AlphaPlayer
from alpha_trainer.classes.AlphaTrainableGame import AlphaTrainableGame


@dataclass
class GamePrototype(AlphaTrainableGame):
    players: tuple[Player]
    board: Board
    current_player: Player

    def copy(self) -> "AlphaTrainableGame":
        pass

    def get_possible_actions(self) -> Generator[AlphaMove, None, None]:
        pass

    def next_turn(self) -> None:
        pass

    def is_terminal(self) -> bool:
        pass

    def get_result(self, player: AlphaPlayer) -> AlphaGameResult:
        pass

    def get_state(self):
        pass

    @classmethod
    def create(cls, n_players: int = 2):
        result = object.__new__(GamePrototype)
        result.board = Board(n_players)
        result.players = tuple(Player() for _ in range(n_players))
        result.current_player = result.players[0]
        return result
