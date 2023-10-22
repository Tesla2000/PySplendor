from itertools import groupby
from pathlib import Path

from PySplendor.data.Card import Card
from PySplendor.data.Tier import Tier


def generate_tiers() -> list[Tier]:
    building_data = iter(Path("PySplendor/buildings.csv").read_text().splitlines())
    next(building_data)
    tiers = list(
        Tier(list(map(Card.from_text, group)))
        for _, group in groupby(building_data, lambda line: line[0])
    )
    return tiers
