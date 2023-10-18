from dataclasses import dataclass, field

from splendor.data.Aristocrat import Aristocrat


@dataclass(slots=True)
class PlayerAristocrats:
    aristocrats: list[Aristocrat] = field(default_factory=list)

    @property
    def points(self) -> int:
        return sum(aristocrat.points for aristocrat in self.aristocrats)

    def append(self, aristocrat: Aristocrat) -> None:
        self.aristocrats.append(aristocrat)
