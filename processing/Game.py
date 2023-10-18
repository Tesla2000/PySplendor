from dataclasses import astuple, fields, asdict
from itertools import combinations, starmap, product, cycle
from typing import Iterable

from alpha_trainer.classes.AlphaMove import AlphaMove
from alpha_trainer.exceptions.GameFinishedException import GameFinishedException
from splendor.data.BasicResources import BasicResources
from splendor.data.Board import Board
from splendor.data.player.Player import Player
from splendor.processing._Game import _Game
from splendor.processing.flatter_recursely import flatter_recursively
from splendor.processing.moves.BuildBoard import BuildBoard
from splendor.processing.moves.BuildReserve import BuildReserve
from splendor.processing.moves.GrabThreeResource import GrabThreeResource
from splendor.processing.moves.ReserveTop import ReserveTop
from splendor.processing.moves.ReserveVisible import ReserveVisible


class Game(_Game):
    _last_turn: bool
    _all_moves: list[AlphaMove]
    _performed_the_last_move: dict[int, bool]

    def __init__(self, n_players: int = 2):
        super().__init__(n_players)
        self._init()

    def _init(self):
        self._performed_the_last_move = dict(
            (id(player), False) for player in self.players
        )
        self._last_turn = False

    def next_turn(self) -> None:
        self.players = next(self.player_order)
        for aristocrat in self.board.aristocrats:
            if not (self.current_player.resources - aristocrat.cost).lacks():
                self.board.aristocrats.remove(aristocrat)
                self.current_player.aristocrats.append(aristocrat)
        if self.current_player.points >= 15 or self._last_turn:
            self._last_turn = True
        self._performed_the_last_move[id(self.current_player)] = self._last_turn
        if all(self._performed_the_last_move.values()):
            winner = max(
                self.players, key=lambda player: (player.points, -len(player.cards))
            )
            raise GameFinishedException(winner)
        self.current_player = self.players[0]

    def get_state(self, expected_length=276) -> list:
        state = flatter_recursively(astuple(self.board))
        for player in self.players:
            state += astuple(player.resources, tuple_factory=list)
            state += astuple(player.production, tuple_factory=list)
            if player != self.current_player:
                state.append(len(player.reserve))
            else:
                state += flatter_recursively(astuple(self.current_player.reserve))
            state.append(player.points)
        if len(state) != expected_length:
            raise ValueError
        return state

    def copy(self) -> "Game":
        board = asdict(self.board)
        players = map(asdict, self.players)
        return Game.from_dict(board, players)

    @property
    def all_moves(self) -> list[AlphaMove]:
        if self._all_moves:
            return self._all_moves
        combos = combinations([{field.name: 1} for field in fields(BasicResources)], 3)
        all_moves = list(
            GrabThreeResource(BasicResources(**res_1, **res_2, **res_3))
            for res_1, res_2, res_3 in combos
        )
        all_moves += list(
            GrabThreeResource(BasicResources(**{field.name: 2}))
            for field in fields(BasicResources)
        )
        all_moves += list(starmap(BuildBoard, product(range(3), range(4))))
        all_moves += list(map(BuildReserve, range(3)))
        all_moves += list(starmap(ReserveVisible, product(range(3), range(4))))
        all_moves += list(map(ReserveTop, range(3)))
        self._all_moves = all_moves
        return all_moves

    @classmethod
    def from_dict(cls, board: dict, players: Iterable[dict]) -> "Game":
        game = object.__new__(Game)
        game.board = Board(**board)
        players = list(Player(**player_state) for player_state in players)
        game.players = players
        game.player_order = sliding_window(cycle(players), len(players))
        game.current_player = players[0]
        game._init()
        return game


n_moves = 45
