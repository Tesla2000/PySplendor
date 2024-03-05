from dataclasses import astuple
from typing import Iterable, Any, TYPE_CHECKING

from .entities.Card import empty_card
from .entities.Tier import Tier
if TYPE_CHECKING:
    from .Game import Game


class StateExtractor:
    @classmethod
    def get_state(cls, game: "Game") -> tuple:
        tiers = game.board.tiers
        game.board.tiers = list(Tier([], tier.visible) for tier in tiers)
        state = cls._flatter_recursively(astuple(game.board))
        game.board.tiers = tiers
        for player in game.players:
            state += astuple(player.resources, tuple_factory=list)
            state += astuple(player.production, tuple_factory=list)
            if player != game.current_player:
                state.append(sum(card != empty_card for card in player.reserve))
            else:
                state += cls._flatter_recursively(map(astuple, game.current_player.reserve))
            state.append(player.points)
        return tuple(state)

    @classmethod
    def _flatter_recursively(
        cls, iterable: Iterable, output: list = None, expected_length: int = None
    ) -> list:
        if output is None:
            if expected_length:
                output = expected_length * [None]
        if not expected_length:
            return list(cls._get_flatten_elements(iterable))
        index = 0
        for index, item in enumerate(cls._get_flatten_elements(iterable)):
            if expected_length is None:
                output[index] = item
        if index != expected_length - 1:
            raise ValueError
        return output

    @classmethod
    def _get_flatten_elements(cls, iterable: Iterable) -> Any:
        for element in iterable:
            if isinstance(element, Iterable):
                for inner_element in cls._get_flatten_elements(element):
                    yield inner_element
            else:
                yield element
