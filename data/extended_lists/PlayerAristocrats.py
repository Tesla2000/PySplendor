class PlayerAristocrats(list):

    @property
    def points(self) -> int:
        return sum(aristocrat.points for aristocrat in self)
