from dataclasses import dataclass, asdict, astuple

from PySplendor.data.BasicResources import BasicResources


@dataclass(slots=True)
class AllResources(BasicResources):
    gold: int = 0

    def __sub__(self, other: "BasicResources") -> "AllResources":
        if not isinstance(other, BasicResources):
            raise ValueError(f"Other element must be resource is {other.__class__}")
        self_dict = asdict(self)
        other_dict = asdict(other)
        resources = AllResources(
            **dict((key, value - other_dict.get(key, 0)) for key, value in self_dict.items())
        )
        resources.gold += sum(map(lambda v: min(0, v), astuple(resources)))
        return resources

    def __rsub__(self, other: "BasicResources") -> "AllResources":
        return self.__sub__(other)

    def lacks(self) -> bool:
        return self.gold < 0
