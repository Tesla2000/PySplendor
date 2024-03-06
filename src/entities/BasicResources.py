from dataclasses import dataclass, asdict
from typing import Self


@dataclass(slots=True, frozen=True)
class BasicResources:
    red: int = 0
    green: int = 0
    blue: int = 0
    black: int = 0
    white: int = 0

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, BasicResources):
            raise ValueError(f"Other element must be resource is {other.__class__}")
        return BasicResources(
            self.red + other.red,
            self.green + other.green,
            self.blue + other.blue,
            self.black + other.black,
            self.white + other.white,
        )
