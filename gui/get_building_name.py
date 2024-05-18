from dataclasses import astuple

from src.entities.BasicResources import BasicResources
from src.entities.Card import Card


def get_building_name(building: Card) -> str:
    prod2str = {
        BasicResources(red=1): "RED",
        BasicResources(green=1): "GREEN",
        BasicResources(blue=1): "BLUE",
        BasicResources(black=1): "BLACK",
        BasicResources(white=1): "WHITE",
    }
    try:
        return "buildings/" + prod2str[building.production] + "".join(map(str, astuple(building.cost)))
    except KeyError:
        return "tier_1"