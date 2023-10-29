import operator
from dataclasses import dataclass, field
from functools import reduce

from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.extended_lists.ExtendedList import ExtendedList


@dataclass
class PlayerCards(ExtendedList):
    _cards: list = field(default_factory=list)

    @property
    def production(self) -> BasicResources:
        return reduce(operator.add, (card.production for card in self._cards), BasicResources())

    @property
    def points(self) -> int:
        return sum(card.points for card in self._cards)
