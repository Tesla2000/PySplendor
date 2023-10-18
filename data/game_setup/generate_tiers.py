from itertools import groupby
from pathlib import Path

from splendor.data.Card import Card
from splendor.data.Tier import Tier


def generate_tiers() -> list[Tier]:
    building_data = iter(Path("splendor/buildings.csv").read_text().splitlines())
    next(building_data)
    tiers = list(
        Tier(list(map(Card.from_text, group)))
        for _, group in groupby(building_data, lambda line: line[0])
    )
    return tiers
