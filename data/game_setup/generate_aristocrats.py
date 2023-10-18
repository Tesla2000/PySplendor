from pathlib import Path

from splendor.data.Aristocrat import Aristocrat


def generate_aristocrats() -> list[Aristocrat]:
    aristocrat_data = Path("splendor/aristocrats.csv").read_text().splitlines()[1:]
    return list(map(Aristocrat.from_text, aristocrat_data))
