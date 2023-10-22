from abc import ABC

from PySplendor.data.BasicResources import BasicResources
from PySplendor.processing.moves.Move import Move


class GrabResource(Move, ABC):
    def __init__(self, resources: BasicResources):
        self.resources = resources

    def __repr__(self):
        return self.resources.__repr__()
