import random
from dataclasses import field, dataclass

from .Card import Card, empty_card


@dataclass(slots=True)
class Tier:
    hidden: list[Card]
    visible: list[Card] = field(default_factory=list)

    def __post_init__(self):
        if not self.visible:
            random.shuffle(self.hidden)
            for _ in range(4):
                self.visible.append(self.hidden.pop())
        self.visible.sort()

    def pop(self, index: int) -> Card:
        card = self.visible.pop(index)
        if self.hidden:
            self.visible.append(self.hidden.pop())
        else:
            self.visible.append(empty_card)
        self.visible.sort()
        return card
