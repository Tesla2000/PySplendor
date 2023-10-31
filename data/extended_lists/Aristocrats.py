from typing_extensions import override

from PySplendor.data.Aristocrat import Aristocrat, empty_aristocrat


class Aristocrats(list):
    @override
    def pop(self, index: int) -> Aristocrat:
        aristocrat = self.pop(index)
        self.append(empty_aristocrat)
        return aristocrat
