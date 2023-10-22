from typing import Iterable

from typing_extensions import override

from PySplendor.data.Card import Card, empty_card


class PlayerReserve(list):

    def __init__(self, iterable: Iterable = None):
        if iterable is None:
            iterable = [empty_card for _ in range(3)]
        super().__init__(iterable)

    def can_add(self) -> bool:
        return empty_card in self

    def append(self, card: Card) -> None:
        if not self.can_add():
            raise ValueError(f"Can't add card to reserve {self}")
        empty_index = self.index(empty_card)
        self[empty_index] = card

    @override
    def pop(self, index: int) -> Card:
        card = self[index]
        if card == empty_card:
            raise ValueError
        self[index] = empty_card
        return card
