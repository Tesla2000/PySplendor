from dataclasses import fields, dataclass, field
from itertools import combinations, starmap, product
from typing import Self, Type

from Config import Config
from .StateExtractor import StateExtractor
from .entities.AllResources import AllResources
from .entities.BasicResources import BasicResources
from .entities.Board import Board
from .entities.Player import Player
from .entities.Tier import Tier
from .entities.extended_lists.Aristocrats import Aristocrats
from .entities.extended_lists.PlayerAristocrats import PlayerAristocrats
from .entities.extended_lists.PlayerCards import PlayerCards
from .entities.extended_lists.PlayerReserve import PlayerReserve
from .moves import (
    Move,
    GrabThreeResource,
    GrabTwoResource,
    BuildBoard,
    BuildReserve,
    ReserveVisible,
    ReserveTop,
    NullMove,
)


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
    _state_extractor: Type[StateExtractor] = StateExtractor

    def __post_init__(self):
        if not self.players:
            self.players = tuple(Player() for _ in range(self.n_players))
        if not self.board:
            self.board = Board(self.n_players)
        if not self._performed_the_last_move:
            self._performed_the_last_move = dict(
                (player, False) for player in self.players
            )
            self.is_blocked = dict((player, False) for player in self.players)
        self.current_player = self.players[0]

    def perform(self, action: Move) -> Self:
        new_state = action.perform(self)
        # if sum(astuple(new_state.current_player.resources)) > 10:
        #     print(self)
        #     print(action)
        #     raise ValueError
        # if sum(sum(astuple(player.resources)) for player in new_state.players) + sum(astuple(new_state.board.resources)) != 25:
        #     print(self)
        #     print(action)
        #     raise ValueError
        # if any(any(r for r in astuple(player.resources) if r < 0) for player in new_state.players) or any(r for r in astuple(new_state.board.resources) if r < 0):
        #     print(self)
        #     print(action)
        #     raise ValueError
        new_state.next_turn()
        return new_state

    def next_turn(self) -> None:
        self.players = (*self.players[1:], self.players[0])
        for index, aristocrat in enumerate(self.board.aristocrats):
            if not (self.current_player.resources - aristocrat.cost).lacks():
                self.current_player.aristocrats.append(
                    self.board.aristocrats.pop(index)
                )
        if self.current_player.points >= Config.min_n_points_to_finish or self._last_turn:
            self._last_turn = True
        self._performed_the_last_move[self.current_player] = self._last_turn
        self.current_player = self.players[0]

    def is_terminal(self) -> bool:
        return all(self._performed_the_last_move.values()) or (
            not any(move for move in self.all_moves if move.is_valid(self))
        )

    def get_results(self) -> dict[int, int]:
        results = {}
        for player in self.players:
            results[player.id] = (
                1
                if player
                   == max(self.players, key=lambda p: (p.points, -len(p.cards)))
                else -1
            )
        return results

    def get_state(self) -> tuple:
        return self._state_extractor.get_state(self)

    def copy(self) -> Self:
        game = Game(
            players=tuple(
                Player(
                    resources=AllResources(
                        (resources := player.resources).red,
                        resources.green,
                        resources.blue,
                        resources.black,
                        resources.white,
                        resources.gold,
                    ),
                    cards=PlayerCards(player.cards),
                    reserve=PlayerReserve(player.reserve),
                    aristocrats=PlayerAristocrats(player.aristocrats),
                    id=player.id,
                )
                for player in self.players
            ),
            board=Board(
                n_players=(board := self.board).n_players,
                tiers=list(Tier(list(tier.hidden), list(tier.visible)) for tier in board.tiers),
                aristocrats=Aristocrats(board.aristocrats),
                resources=AllResources(
                    board.resources.red,
                    board.resources.green,
                    board.resources.blue,
                    board.resources.black,
                    board.resources.white,
                    board.resources.gold,
                ),
            ),
            n_players=self.n_players,
            _last_turn=self._last_turn,
        )
        game.current_player = game.players[0]
        for player in game.players:
            game.is_blocked[player] = next(
                value for key, value in self.is_blocked.items() if key == player
            )
            game._performed_the_last_move[player] = next(
                value for key, value in self._performed_the_last_move.items() if key == player
            )
        return game

    def get_possible_actions(self) -> tuple[Move, ...]:
        return tuple(move for move in self.all_moves if move.is_valid(self))

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
