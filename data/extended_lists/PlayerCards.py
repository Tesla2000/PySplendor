import operator
from functools import reduce

from PySplendor.data.BasicResources import BasicResources


class PlayerCards(list):

    @property
    def production(self) -> BasicResources:
        return reduce(operator.add, (card.production for card in self), BasicResources())

    @property
    def points(self) -> int:
        return sum(card.points for card in self)
