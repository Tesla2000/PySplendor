from dataclasses import dataclass, field
from random import randint

from PySplendor.data.AllResources import AllResources
from PySplendor.data.Aristocrat import Aristocrat
from PySplendor.data.BasicResources import BasicResources
from PySplendor.data.Card import Card
from PySplendor.data.extended_lists.PlayerAristocrats import PlayerAristocrats
from PySplendor.data.extended_lists.PlayerCards import PlayerCards
from PySplendor.data.extended_lists.PlayerReserve import PlayerReserve
from alpha_trainer.classes.AlphaPlayer import AlphaPlayer


@dataclass(slots=True)
class Player(AlphaPlayer):
    id: int = field(default_factory=lambda: randint(0, 2 ** 63))
    resources: AllResources = field(default_factory=AllResources)
    cards: PlayerCards = field(default_factory=PlayerCards)
    reserve: PlayerReserve = field(default_factory=PlayerReserve)
    aristocrats: PlayerAristocrats = field(default_factory=PlayerAristocrats)

    def __post_init__(self):
        if isinstance(self.resources, dict):
            self.resources = AllResources(**self.resources)
        self.cards = PlayerCards(list(Card(**card) if isinstance(card, dict) else card for card in self.cards))
        self.reserve = PlayerReserve(list(Card(**card) if isinstance(card, dict) else card for card in self.reserve))
        self.aristocrats = PlayerAristocrats(
            list(Aristocrat(**aristocrat) if isinstance(aristocrat, dict) else aristocrat for aristocrat in self.aristocrats))

    @property
    def points(self) -> int:
        return self.cards.points + self.aristocrats.points

    @property
    def production(self) -> BasicResources:
        return self.cards.production
