from ..Aristocrat import Aristocrat, empty_aristocrat


class Aristocrats(list):
    def pop(self, index: int) -> Aristocrat:
        aristocrat = super().pop(index)
        self.append(empty_aristocrat)
        return aristocrat
