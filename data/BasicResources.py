from dataclasses import dataclass, asdict


@dataclass(slots=True)
class BasicResources:
    red: int = 0
    green: int = 0
    blue: int = 0
    black: int = 0
    white: int = 0

    def __add__(self, other: "BasicResources") -> "BasicResources":
        if not isinstance(other, BasicResources):
            raise ValueError(f"Other element must be resource is {other.__class__}")
        self_dict = asdict(self)
        other_dict = asdict(other)
        return BasicResources(
            **dict((key, value + other_dict[key]) for key, value in self_dict.items())
        )
