from abc import ABC

from splendor.data.BasicResources import BasicResources
from splendor.processing.moves.Move import Move


class GrabResource(Move, ABC):
    def __init__(self, resources: BasicResources):
        self.resources = resources

    def __repr__(self):
        return self.resources.__repr__()
