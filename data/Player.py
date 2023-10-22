from dataclasses import dataclass, field

from PySplendor.data.AllResources import AllResources
from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.extended_lists.PlayerAristocrats import PlayerAristocrats
from PySplendor.data.extended_lists.PlayerCards import PlayerCards
from PySplendor.data.extended_lists.PlayerReserve import PlayerReserve


@dataclass(slots=True, eq=False)
class Player:
    resources: AllResources = field(default_factory=AllResources)
    cards: PlayerCards = field(default_factory=PlayerCards)
    reserve: PlayerReserve = field(default_factory=PlayerReserve)
    aristocrats: PlayerAristocrats = field(default_factory=PlayerAristocrats)

    @property
    def points(self) -> int:
        return self.cards.points + self.aristocrats.points

    @property
    def production(self) -> BasicResources:
        return self.cards.production
