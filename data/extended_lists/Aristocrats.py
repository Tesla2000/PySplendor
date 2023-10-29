from dataclasses import dataclass

from PySplendor.data.Aristocrat import Aristocrat, empty_aristocrat
from PySplendor.data.extended_lists.ExtendedList import ExtendedList


@dataclass
class Aristocrats(ExtendedList):
    _aristocrats: list[Aristocrat]

    def pop(self, index: int) -> "Aristocrat":
        aristocrat = self._aristocrats.pop(index)
        self._aristocrats.append(empty_aristocrat)
        return aristocrat
