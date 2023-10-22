from abc import ABC
from itertools import cycle

from more_itertools import sliding_window

from PySplendor.data.Board import Board
from PySplendor.data.Player import Player
from alpha_trainer.classes.AlphaTrainableGame import AlphaTrainableGame


class GamePrototype(AlphaTrainableGame, ABC):
    players: tuple[Player]
    board: Board
    current_player: Player

    def __init__(self, n_players: int = 2):
        players = list(Player() for _ in range(n_players))
        self.board = Board(n_players)
        self.player_order = sliding_window(cycle(players), n_players)
        self.players = next(self.player_order)
        self.current_player = self.players[0]
