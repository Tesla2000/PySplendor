from dataclasses import dataclass, field

from splendor.data.AllResources import AllResources
from splendor.data.BasicResources import BasicResources
from splendor.data.player.PlayerAristocrats import PlayerAristocrats
from splendor.data.player.PlayerCards import PlayerCards
from splendor.data.player.PlayerReserve import PlayerReserve


@dataclass(slots=True)
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
