from dataclasses import dataclass

from PySplendor.data.BasicResources import BasicResources


@dataclass(slots=True)
class Aristocrat:
    points: int
    cost: BasicResources

    @classmethod
    def from_text(cls, line: str) -> "Aristocrat":
        points, white, blue, green, red, black = map(int, line.split(","))
        cost = BasicResources(red, green, blue, black, white)
        return Aristocrat(points, cost)


empty_aristocrat = Aristocrat(0, BasicResources())
