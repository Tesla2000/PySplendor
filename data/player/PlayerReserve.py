from dataclasses import dataclass, field

from splendor.data.Card import Card, empty_card


@dataclass(slots=True)
class PlayerReserve:
    cards: list[Card] = field(
        default_factory=lambda: [empty_card, empty_card, empty_card]
    )

    def can_add(self) -> bool:
        return empty_card in self.cards

    def append(self, card: Card) -> None:
        if not self.can_add():
            raise ValueError(f"Can't add card to reserve {self.cards}")
        empty_index = self.cards.index(empty_card)
        self.cards[empty_index] = card

    def pop(self, index: int) -> Card:
        cards = list(self.cards)
        card = cards[index]
        if card == empty_card:
            raise ValueError
        cards[index] = empty_card
        return card

    def __getitem__(self, item) -> Card:
        return self.cards.__getitem__(item)

    def __len__(self) -> int:
        return len(self.cards)
