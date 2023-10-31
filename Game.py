from dataclasses import astuple, fields, asdict, dataclass
from itertools import combinations, starmap, product
from typing import Generator

from PySplendor.dacite.dacite.core import from_dict
from PySplendor.data.AllResources import AllResources
from PySplendor.data.Aristocrat import Aristocrat
from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.Board import Board
from PySplendor.data.Card import empty_card, Card
from PySplendor.data.Player import Player
from PySplendor.data.Tier import Tier
from PySplendor.data.extended_lists.Aristocrats import Aristocrats
from PySplendor.data.extended_lists.PlayerAristocrats import PlayerAristocrats
from PySplendor.data.extended_lists.PlayerCards import PlayerCards
from PySplendor.data.extended_lists.PlayerReserve import PlayerReserve
from PySplendor.processing.flatter_recursely import flatter_recursively
from PySplendor.processing.moves.BuildBoard import BuildBoard
from PySplendor.processing.moves.BuildReserve import BuildReserve
from PySplendor.processing.moves.GrabThreeResource import GrabThreeResource
from PySplendor.processing.moves.ReserveTop import ReserveTop
from PySplendor.processing.moves.ReserveVisible import ReserveVisible
from alpha_trainer.classes.AlphaGameResult import AlphaGameResult
from alpha_trainer.classes.AlphaMove import AlphaMove
from alpha_trainer.classes.AlphaTrainableGame import AlphaTrainableGame

max_turns = 0


@dataclass
class Game(AlphaTrainableGame):
    players: tuple[Player]
    board: Board
    current_player: Player
    _turn_counter: int = 0
    _performed_the_last_move: dict = None
    _last_turn: bool = False

    @classmethod
    def create(cls, n_players: int = 2):
        result = object.__new__(Game)
        result.players = tuple(Player() for _ in range(n_players))
        result.board = Board(n_players)
        result.current_player = result.players[0]
        result._performed_the_last_move = dict(
            (player.id, False) for player in result.players
        )
        result._last_turn = False
        return result

    def next_turn(self) -> None:
        self.players = (*self.players[1:], self.players[0])
        for index, aristocrat in enumerate(self.board.aristocrats):
            if not (self.current_player.resources - aristocrat.cost).lacks():
                self.current_player.aristocrats.append(self.board.aristocrats.pop(index))
        if self.current_player.points >= 15 or self._last_turn:
            self._last_turn = True
        self._performed_the_last_move[self.current_player.id] = self._last_turn
        self.current_player = self.players[0]
        self._turn_counter += 1

    def is_terminal(self) -> bool:
        return all(self._performed_the_last_move.values()) or (not all(self.get_possible_actions()))

    def get_result(self, player: Player) -> AlphaGameResult:
        global max_turns
        if max_turns < self._turn_counter:
            max_turns = self._turn_counter
            print(max_turns)
        speed_modifier = 1 + (self._turn_counter / len(self.players))
        if not all(self._performed_the_last_move.values()):
            return AlphaGameResult(0 if player != self.current_player else -1 / speed_modifier)
        players_in_order = sorted(
            self.players, key=lambda player_instance: (player_instance.points, -len(player_instance.cards)),
            reverse=True
        )
        max_points = players_in_order[0].points
        point_differences = tuple(player.points - max_points for player in players_in_order)
        if players_in_order[0] == player:
            score = (-point_differences[1] / max_points) / speed_modifier
        else:
            score = point_differences[players_in_order.index(player)] / speed_modifier
        return AlphaGameResult(score)

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
        return eval(str(self))

    def get_possible_actions(self) -> Generator[AlphaMove, None, None]:
        return (move for move in _all_moves if move.is_valid(self))


combos = combinations([{field.name: 1} for field in fields(BasicResources)], 3)
_all_moves = list(
    GrabThreeResource(BasicResources(**res_1, **res_2, **res_3))
    for res_1, res_2, res_3 in combos
)
_all_moves += list(
    GrabThreeResource(BasicResources(**{field.name: 2}))
    for field in fields(BasicResources)
)
_all_moves += list(starmap(BuildBoard, product(range(3), range(4))))
_all_moves += list(map(BuildReserve, range(3)))
_all_moves += list(starmap(ReserveVisible, product(range(3), range(4))))
_all_moves += list(map(ReserveTop, range(3)))
n_moves = len(_all_moves)

if __name__ == '__main__':
    g = Game.create()
    copy = eval(str(g))
