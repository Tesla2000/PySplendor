import random
from dataclasses import field, dataclass

from splendor.data.Card import Card, empty_card


@dataclass(slots=True)
class Tier:
    hidden: list[Card]
    visible: list[Card] = field(default_factory=list)

    def __post_init__(self):
        self.hidden = list(
            Card(**card) if isinstance(card, dict) else card for card in self.hidden
        )
        self.visible = list(
            Card(**card) if isinstance(card, dict) else card for card in self.visible
        )
        if not self.visible:
            random.shuffle(self.hidden)
            for _ in range(4):
                self.visible.append(self.hidden.pop())

    def pop(self, index: int) -> Card:
        card = self.visible.pop(index)
        if self.hidden:
            self.visible.append(self.hidden.pop())
        else:
            self.visible.append(empty_card)
        return card
