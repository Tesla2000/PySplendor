import random
from pathlib import Path

from ..Aristocrat import Aristocrat
from ..extended_lists.Aristocrats import Aristocrats


def generate_aristocrats() -> Aristocrats:
    aristocrat_data = Path(__file__).parents[2].joinpath("aristocrats.csv").read_text().splitlines()[1:]
    aristocrats = list(map(Aristocrat.from_text, aristocrat_data))
    random.shuffle(aristocrats)
    return Aristocrats(aristocrats)
