from dataclasses import astuple, fields, asdict
from itertools import combinations, starmap, product, cycle
from typing import Iterable, Generator

from more_itertools import sliding_window

from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.Board import Board
from PySplendor.data.Card import empty_card
from PySplendor.data.Player import Player
from PySplendor.data.Tier import Tier
from PySplendor.processing.GamePrototype import GamePrototype
from PySplendor.processing.flatter_recursely import flatter_recursively
from PySplendor.processing.moves.BuildBoard import BuildBoard
from PySplendor.processing.moves.BuildReserve import BuildReserve
from PySplendor.processing.moves.GrabThreeResource import GrabThreeResource
from PySplendor.processing.moves.ReserveTop import ReserveTop
from PySplendor.processing.moves.ReserveVisible import ReserveVisible
from alpha_trainer.classes.AlphaGameResult import AlphaGameResult
from alpha_trainer.classes.AlphaMove import AlphaMove
from alpha_trainer.classes.AlphaPlayer import AlphaPlayer


class Game(GamePrototype):
    _last_turn: bool = None
    _all_moves: list[AlphaMove] = None
    _performed_the_last_move: dict[int, bool] = None

    def __init__(self, n_players: int = 2):
        super().__init__(n_players)
        self._init()

    def _init(self):
        self._performed_the_last_move = dict(
            (player.id, False) for player in self.players
        )
        self._last_turn = False

    def next_turn(self) -> None:
        self.players = next(self.player_order)
        for index, aristocrat in enumerate(self.board.aristocrats):
            if not (self.current_player.resources - aristocrat.cost).lacks():
                self.current_player.aristocrats.append(self.board.aristocrats.pop(index))
        if self.current_player.points >= 15 or self._last_turn:
            self._last_turn = True
        self._performed_the_last_move[self.current_player.id] = self._last_turn
        self.current_player = self.players[0]

    def is_terminal(self) -> bool:
        return all(self._performed_the_last_move.values()) or (not all(self.get_possible_actions()))

    def get_result(self, player: AlphaPlayer) -> AlphaGameResult:
        if all(self._performed_the_last_move.values()):
            winner = max(
                self.players, key=lambda player: (player.points, -len(player.cards))
            )
            return AlphaGameResult(1 if winner == player else -1)
        return AlphaGameResult(-1 if self.current_player == player else 1)

    def get_state(self) -> list:
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
        return state

    def copy(self) -> "Game":
        board = asdict(self.board)
        players = map(asdict, self.players)
        return Game.from_dict(board, players)

    def get_possible_actions(self) -> Generator[AlphaMove, None, None]:
        if self._all_moves:
            return (move for move in self._all_moves if move.is_valid(self))
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
        return (move for move in self._all_moves if move.is_valid(self))

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
