from dataclasses import dataclass, asdict, fields, astuple
from typing import Self

from .BasicResources import BasicResources


@dataclass(slots=True, frozen=True)
class AllResources(BasicResources):
    gold: int = 0

    def __sub__(self, other: BasicResources) -> Self:
        if not isinstance(other, BasicResources):
            raise ValueError(f"Other element must be resource is {other.__class__}")
        self_dict = asdict(self)
        other_dict = asdict(other)
        resources = AllResources(
            **dict(
                (key, value - other_dict.get(key, 0))
                for key, value in self_dict.items()
            )
        )
        resources = AllResources(
            *tuple(max(0, resource) for resource in astuple(resources)[:-1]),
            resources.gold + sum(
                min(0, getattr(resources, field.name)) for field in fields(BasicResources)
            ),
        )
        return resources

    def __rsub__(self, other: BasicResources) -> Self:
        return self.__sub__(other)

    def lacks(self) -> bool:
        return self.gold < 0
