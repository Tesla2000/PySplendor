import random
from dataclasses import dataclass, field

from PySplendor.data.AllResources import AllResources
from PySplendor.data.Aristocrat import Aristocrat
from PySplendor.data.extended_lists.Aristocrats import Aristocrats
from PySplendor.data.Tier import Tier
from PySplendor.data.game_setup.generate_aristocrats import generate_aristocrats
from PySplendor.data.game_setup.generate_tiers import generate_tiers


@dataclass(slots=True)
class Board:
    n_players: int = 2
    tiers: list[Tier] = field(default_factory=generate_tiers)
    aristocrats: Aristocrats = field(default_factory=generate_aristocrats)
    resources: AllResources = field(default=None)

    def __post_init__(self):
        if self.resources is None:
            self.resources = AllResources(*5 * [{2: 4, 3: 5, 4: 7}[self.n_players]])
            self.resources.gold = 5
        if isinstance(self.resources, dict):
            self.resources = AllResources(**self.resources)
        self.aristocrats = Aristocrats(
            Aristocrat(**aristocrat) if isinstance(aristocrat, dict) else aristocrat
            for aristocrat in self.aristocrats
        )
        if len(self.aristocrats) != self.n_players + 1:
            random.shuffle(self.aristocrats)
            self.aristocrats = Aristocrats(self.aristocrats[: self.n_players + 1])
        self.tiers = list(
            Tier(**tier) if isinstance(tier, dict) else tier for tier in self.tiers
        )
