from dataclasses import dataclass, field

from .AllResources import AllResources
from .Aristocrat import Aristocrat
from .BasicResources import BasicResources
from .Card import Card
from .extended_lists.PlayerAristocrats import PlayerAristocrats
from .extended_lists.PlayerCards import PlayerCards
from .extended_lists.PlayerReserve import PlayerReserve


@dataclass(slots=True)
class Player:
    resources: AllResources = field(default_factory=AllResources)
    cards: PlayerCards[Card] = field(default_factory=PlayerCards)
    reserve: PlayerReserve[Card] = field(default_factory=PlayerReserve)
    aristocrats: PlayerAristocrats[Aristocrat] = field(
        default_factory=PlayerAristocrats
    )

    def __post_init__(self):
        if isinstance(self.resources, dict):
            self.resources = AllResources(**self.resources)
        self.cards = PlayerCards(
            list(
                Card(**card) if isinstance(card, dict) else card for card in self.cards
            )
        )
        self.reserve = PlayerReserve(
            list(
                Card(**card) if isinstance(card, dict) else card
                for card in self.reserve
            )
        )
        self.aristocrats = PlayerAristocrats(
            list(
                Aristocrat(**aristocrat) if isinstance(aristocrat, dict) else aristocrat
                for aristocrat in self.aristocrats
            )
        )

    @property
    def points(self) -> int:
        return self.cards.points + self.aristocrats.points

    @property
    def production(self) -> BasicResources:
        return self.cards.production

    def __hash__(self):
        return id(self)
