from db.SpeedSample import SpeedSample
from db.session import session


def save_speed_sample(states: list[tuple[int]]) -> tuple[SpeedSample, ...]:
    speed_samples = tuple(SpeedSample(state=state, turns_till_end=move_till_end, move_index=int(move_index)) for move_till_end, (state, move_index) in enumerate(reversed(states), 1))
    # session.add_all(speed_samples)
    # session.commit()
    return speed_samples
