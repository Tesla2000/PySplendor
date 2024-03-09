from dataclasses import dataclass
from typing import Self

from .BasicResources import BasicResources


@dataclass(slots=True, frozen=True)
class AllResources(BasicResources):
    gold: int = 0

    def __sub__(self, other: BasicResources) -> Self:
        if not isinstance(other, BasicResources):
            raise ValueError(f"Other element must be resource is {other.__class__}")
        return AllResources(
            max(0, self.red - other.red),
            max(0, self.green - other.green),
            max(0, self.blue - other.blue),
            max(0, self.black - other.black),
            max(0, self.white - other.white),
            self.gold
            + sum(
                (
                    min(0, self.red - other.red),
                    min(0, self.green - other.green),
                    min(0, self.blue - other.blue),
                    min(0, self.black - other.black),
                    min(0, self.white - other.white),
                )
            ),
        )

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, BasicResources):
            raise ValueError(f"Other element must be resource is {other.__class__}")
        return AllResources(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue,
            self.black + other.black,
            self.white + other.white,
            self.gold + getattr(other, "gold", 0),
        )

    def __rsub__(self, other: BasicResources) -> Self:
        return self.__sub__(other)

    def lacks(self) -> bool:
        return self.gold < 0

    def __iter__(self):
        return (
            self.red,
            self.green,
            self.blue,
            self.black,
            self.white,
            self.gold,
        ).__iter__()


if __name__ == "__main__":
    (
        AllResources(red=0, green=0, blue=0, black=4, white=4, gold=5)
        - BasicResources(red=1, green=1, blue=0, black=0, white=1)
    )
