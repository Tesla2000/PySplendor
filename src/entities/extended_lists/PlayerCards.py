from ..BasicResources import BasicResources


class PlayerCards(list):
    @property
    def production(self) -> BasicResources:
        if not self:
            return BasicResources()
        return BasicResources(
            sum(card.production.red for card in self),
            sum(card.production.green for card in self),
            sum(card.production.blue for card in self),
            sum(card.production.black for card in self),
            sum(card.production.white for card in self),
        )

    @property
    def points(self) -> int:
        return sum(card.points for card in self)
