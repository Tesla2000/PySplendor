from dataclasses import dataclass, field

from PySplendor.data.Card import Card, empty_card
from PySplendor.data.extended_lists.ExtendedList import ExtendedList


@dataclass
class PlayerReserve(ExtendedList):
    _cards: list[Card] = field(default_factory=lambda: list(empty_card for _ in range(3)))

    def can_add(self) -> bool:
        return empty_card in self._cards

    def append(self, card: Card) -> None:
        if not self.can_add():
            raise ValueError(f"Can't add card to reserve {self}")
        empty_index = self._cards.index(empty_card)
        self._cards[empty_index] = card

    def pop(self, index: int) -> Card:
        card = self._cards[index]
        if card == empty_card:
            raise ValueError
        self._cards[index] = empty_card
        return card
