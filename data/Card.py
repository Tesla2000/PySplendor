from splendor.data.BasicResources import BasicResources
from dataclasses import dataclass


@dataclass(slots=True)
class Card:
    production: BasicResources
    cost: BasicResources
    points: int = 0

    def __post_init__(self):
        if isinstance(self.production, dict):
            self.production = BasicResources(**self.production)
        if isinstance(self.cost, dict):
            self.cost = BasicResources(**self.cost)

    @classmethod
    def from_text(cls, line: str) -> "Card":
        tier, production, points, name, white, blue, green, red, black = line.split(",")
        cost = BasicResources(*tuple(map(int, (red, green, blue, black, white))))
        production = BasicResources(**{production: 1})
        return Card(production, cost, int(points))


empty_card = Card(BasicResources(), BasicResources(), -1)
