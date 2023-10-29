from dataclasses import dataclass

from PySplendor.data.Aristocrat import Aristocrat, empty_aristocrat
from PySplendor.data.extended_lists.ExtendedList import ExtendedList


@dataclass
class Aristocrats(ExtendedList):
    _aristocrats: list

    def pop(self, index: int) -> "Aristocrat":
        aristocrat = self._aristocrats.pop(index)
        self._aristocrats.append(empty_aristocrat)
        return aristocrat


if __name__ == '__main__':
    a = Aristocrats([1, 2, 3])
    assert len(a) == 3
    a.append(4)
    assert len(a) == 4
    a.pop(0)
    assert len(a) == 4
    assert a[-1] == empty_aristocrat
