from abc import ABC
from dataclasses import dataclass

from src.entities.BasicResources import BasicResources
from .Move import Move


@dataclass(slots=True)
class GrabResource(Move, ABC):
    resources: BasicResources

    def __repr__(self):
        return self.resources.__repr__()
