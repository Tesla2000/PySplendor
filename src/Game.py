from dataclasses import astuple, fields, asdict, dataclass, field
from itertools import combinations, starmap, product
from typing import Self, Iterable, Any
from dacite import from_dict

from .entities.BasicResources import BasicResources
from .entities.Board import Board
from .entities.Card import empty_card
from .entities.Player import Player
from .entities.Tier import Tier
from .moves import Move, GrabThreeResource, GrabTwoResource, BuildBoard, BuildReserve, ReserveVisible, ReserveTop, \
    NullMove


@dataclass(slots=True)
class Game:
    players: tuple[Player, ...] = field(default=None)
    board: Board = field(default=None)
    n_players: int = field(default=2)
    current_player: Player = field(init=False)
    is_blocked: dict = None
    _turn_counter: int = 0
    _performed_the_last_move: dict = None
    _last_turn: bool = False

    def __post_init__(self):
        if not self.board or not self.players:
            self.players = tuple(Player() for _ in range(self.n_players))
            self.board = Board(self.n_players)
            self._performed_the_last_move = dict(
                (player, False) for player in self.players
            )
            self.is_blocked = dict(
                (player, False) for player in self.players
            )
            self._last_turn = False
        self.current_player = self.players[0]

    def perform(self, action: Move) -> Self:
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
        self._performed_the_last_move[self.current_player] = self._last_turn
        self.current_player = self.players[0]
        self._turn_counter += 1

    def is_terminal(self) -> bool:
        return all(self._performed_the_last_move.values()) or (
            not self.get_possible_actions()
        )

    def get_results(self) -> dict[Player, bool]:
        results = {}
        for player in self.players:
            if not all(self._performed_the_last_move.values()):
                results[player] = player == max(self.players, key=lambda p: (p.points, -len(p.cards)))
            else:
                print("Finished game")
        return results

    def get_state(self) -> tuple:
        tiers = self.board.tiers
        self.board.tiers = list(Tier([], tier.visible) for tier in tiers)
        state = self._flatter_recursively(astuple(self.board))
        self.board.tiers = tiers
        for player in self.players:
            state += astuple(player.resources, tuple_factory=list)
            state += astuple(player.production, tuple_factory=list)
            if player != self.current_player:
                state.append(sum(card != empty_card for card in player.reserve))
            else:
                state += self._flatter_recursively(map(astuple, self.current_player.reserve))
            state.append(player.points)
        return tuple(state)

    def copy(self) -> Self:
        game = from_dict(Game, asdict(self))
        game.current_player = game.players[0]
        return game

    def get_possible_actions(self) -> list[Move]:
        return list(move for move in self.all_moves if move.is_valid(self))

    def _flatter_recursively(
        self, iterable: Iterable, output: list = None, expected_length: int = None
    ) -> list:
        if output is None:
            if expected_length:
                output = expected_length * [None]
        if not expected_length:
            return list(self._get_flatten_elements(iterable))
        index = 0
        for index, item in enumerate(self._get_flatten_elements(iterable)):
            if expected_length is None:
                output[index] = item
        if index != expected_length - 1:
            raise ValueError
        return output

    def _get_flatten_elements(self, iterable: Iterable) -> Any:
        for element in iterable:
            if isinstance(element, Iterable):
                for inner_element in self._get_flatten_elements(element):
                    yield inner_element
            else:
                yield element

    combos = combinations([{field.name: 1} for field in fields(BasicResources)], 3)
    all_moves = list(
        GrabThreeResource(BasicResources(**res_1, **res_2, **res_3))
        for res_1, res_2, res_3 in combos
    )
    del combos
    all_moves += list(
        GrabTwoResource(BasicResources(**{field.name: 2}))
        for field in fields(BasicResources)
    )
    all_moves += list(starmap(BuildBoard, product(range(3), range(4))))
    all_moves += list(map(BuildReserve, range(3)))
    all_moves += list(starmap(ReserveVisible, product(range(3), range(4))))
    all_moves += list(map(ReserveTop, range(3)))
    all_moves.append(NullMove())
    all_moves = tuple(all_moves)
