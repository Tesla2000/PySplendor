from dataclasses import dataclass, field

from PySplendor.data.extended_lists.ExtendedList import ExtendedList


@dataclass
class PlayerAristocrats(ExtendedList):
    aristocrats: list = field(default_factory=list)

    @property
    def points(self) -> int:
        return sum(aristocrat.points for aristocrat in self.aristocrats)
