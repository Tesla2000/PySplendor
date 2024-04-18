from typing import NamedTuple, Sequence


class GameSample(NamedTuple):
    state: Sequence[int]
    policy: Sequence[float]
    wins: int
