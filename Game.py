from dataclasses import astuple, fields, asdict, dataclass, field
from itertools import combinations, starmap, product
from typing import Self

from PySplendor.dacite.dacite import Config
from PySplendor.dacite.dacite.core import from_dict
from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.Board import Board
from PySplendor.data.Card import empty_card
from PySplendor.data.Player import Player
from PySplendor.data.Tier import Tier
from PySplendor.processing.flatter_recursely import flatter_recursively
from PySplendor.processing.moves.BuildBoard import BuildBoard
from PySplendor.processing.moves.BuildReserve import BuildReserve
from PySplendor.processing.moves.GrabThreeResource import GrabThreeResource
from PySplendor.processing.moves.GrabTwoResource import GrabTwoResource
from PySplendor.processing.moves.ReserveTop import ReserveTop
from PySplendor.processing.moves.ReserveVisible import ReserveVisible
from alpha_trainer.classes.AlphaGameResult import AlphaGameResult
from alpha_trainer.classes.AlphaMove import AlphaMove
from alpha_trainer.classes.AlphaTrainableGame import (
    AlphaTrainableGame,
    AlphaGameResults,
)


@dataclass
class Game(AlphaTrainableGame):
    players: tuple[Player] = field(default=None)
    board: Board = field(default=None)
    n_players: int = field(default=2)
    current_player: Player = field(init=False)
    _turn_counter: int = 0
    _performed_the_last_move: dict = None
    _last_turn: bool = False

    def __post_init__(self):
        if not self.board or not self.players:
            self.players = tuple(Player() for _ in range(self.n_players))
            self.board = Board(self.n_players)
            self._performed_the_last_move = dict(
                (player.id, False) for player in self.players
            )
            self._last_turn = False
        self.current_player = self.players[0]

    def perform(self, action: "AlphaMove") -> Self:
        action.perform(self)
        self.next_turn()
        return self

    def next_turn(self) -> None:
        self.players = (*self.players[1:], self.players[0])
        for index, aristocrat in enumerate(self.board.aristocrats):
            if not (self.current_player.resources - aristocrat.cost).lacks():
                self.current_player.aristocrats.append(
                    self.board.aristocrats.pop(index)
                )
        if self.current_player.points >= 15 or self._last_turn:
            self._last_turn = True
        self._performed_the_last_move[self.current_player.id] = self._last_turn
        self.current_player = self.players[0]
        self._turn_counter += 1

    def is_terminal(self) -> bool:
        return all(self._performed_the_last_move.values()) or (
            not self.get_possible_actions()
        )

    def get_results(self) -> AlphaGameResults:
        results = {}
        for player in self.players:
            if not all(self._performed_the_last_move.values()):
                results[player.id] = AlphaGameResult(
                    1 if player.id != self.current_player.id else -1
                )
            else:
                print("Finished game")
        return results

    def get_state(self) -> tuple:
        tiers = self.board.tiers
        self.board.tiers = list(Tier([], tier.visible) for tier in tiers)
        state = flatter_recursively(astuple(self.board))
        self.board.tiers = tiers
        for player in self.players:
            state += astuple(player.resources, tuple_factory=list)
            state += astuple(player.production, tuple_factory=list)
            if player != self.current_player:
                state.append(sum(card != empty_card for card in player.reserve))
            else:
                state += flatter_recursively(map(astuple, self.current_player.reserve))
            state.append(player.points)
        return tuple(state)

    def copy(self) -> "Game":
        game = from_dict(Game, asdict(self), Config(check_types=False))
        game.current_player = game.players[0]
        return game

    def get_possible_actions(self) -> list[AlphaMove]:
        return list(move for move in _all_moves if move.is_valid(self))


combos = combinations([{field.name: 1} for field in fields(BasicResources)], 3)
_all_moves = list(
    GrabThreeResource(BasicResources(**res_1, **res_2, **res_3))
    for res_1, res_2, res_3 in combos
)
_all_moves += list(
    GrabTwoResource(BasicResources(**{field.name: 2}))
    for field in fields(BasicResources)
)
_all_moves += list(starmap(BuildBoard, product(range(3), range(4))))
_all_moves += list(map(BuildReserve, range(3)))
_all_moves += list(starmap(ReserveVisible, product(range(3), range(4))))
_all_moves += list(map(ReserveTop, range(3)))
n_moves = len(_all_moves)
