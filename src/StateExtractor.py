from dataclasses import astuple
from itertools import chain
from typing import Iterable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .Game import Game


class StateExtractor:
    @classmethod
    def get_state(cls, game: "Game") -> tuple:
        return tuple(
            chain.from_iterable(
                (
                    chain.from_iterable(
                        (*astuple(card.cost), *astuple(card.production), card.points)
                        for tier in game.board.tiers
                        for card in tier.visible
                    ),
                    chain.from_iterable(
                        (*astuple(card.cost), *astuple(card.production), card.points)
                        for card in game.current_player.reserve
                    ),
                    chain.from_iterable(
                        astuple(aristocrat.cost)
                        for aristocrat in game.board.aristocrats
                    ),
                    chain.from_iterable(
                        (
                            *astuple(player.resources),
                            *astuple(player.production),
                            player.points,
                        )
                        for player in game.players
                    ),
                    (len(player.reserve) for player in game.players[1:]),
                )
            )
        )

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
