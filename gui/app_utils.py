from dataclasses import astuple, asdict

from src.entities.BasicResources import BasicResources
from src.entities.Card import Card

prod2str = {
    BasicResources(red=1): "RED",
    BasicResources(green=1): "GREEN",
    BasicResources(blue=1): "BLUE",
    BasicResources(black=1): "BLACK",
    BasicResources(white=1): "WHITE",
}


def get_building_name(building: Card) -> str:
    try:
        return "buildings/" + prod2str[building.production] + "".join(
            map(str, astuple(building.cost)))
    except KeyError:
        return "tier_1"


def card_to_dict(card: Card):
    return dict(points=card.points, **asdict(card.cost),
                production=prod2str[card.production])
