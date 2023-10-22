from pathlib import Path

from PySplendor.data.Aristocrat import Aristocrat
from PySplendor.data.extended_lists.Aristocrats import Aristocrats


def generate_aristocrats() -> Aristocrats:
    aristocrat_data = Path("PySplendor/aristocrats.csv").read_text().splitlines()[1:]
    return Aristocrats(map(Aristocrat.from_text, aristocrat_data))
