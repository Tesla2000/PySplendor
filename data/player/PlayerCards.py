from collections import Counter
from dataclasses import dataclass, field

from splendor.data.Card import Card
from splendor.data.BasicResources import BasicResources


@dataclass(slots=True)
class PlayerCards:
    cards: list[Card] = field(default_factory=list)

    @property
    def production(self) -> BasicResources:
        return BasicResources(**Counter(card.production.value for card in self.cards))

    @property
    def points(self) -> int:
        return sum(card.points for card in self.cards)

    def append(self, card: Card) -> None:
        self.cards.append(card)

    def __len__(self):
        return len(self.cards)
