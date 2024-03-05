from .hashablelist import hashablelist


class PlayerAristocrats(hashablelist):
    @property
    def points(self) -> int:
        return sum(aristocrat.points for aristocrat in self)
