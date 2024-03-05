from itertools import filterfalse
from typing import Iterable

from ..Card import Card, empty_card
from .hashablelist import hashablelist


class PlayerReserve(hashablelist):
    def __init__(self, iterable: Iterable = None):
        super().__init__(iterable or (empty_card for _ in range(3)))

    def can_add(self) -> bool:
        return empty_card in self

    def append(self, card: Card) -> None:
        if not self.can_add():
            raise ValueError(f"Can't add card to reserve {self}")
        empty_index = self.index(empty_card)
        self[empty_index] = card

    def pop(self, index: int) -> Card:
        card = self[index]
        if card == empty_card:
            raise ValueError
        self[index] = empty_card
        return card

    def __len__(self):
        return len(tuple(filterfalse(empty_card.__eq__, self)))
