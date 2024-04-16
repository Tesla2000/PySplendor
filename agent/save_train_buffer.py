import numpy as np
from sqlalchemy import func

from Config import Config
from db.Game import Game
from db.Sample import Sample
from db.session import session


def save_train_buffer(buffer: list[tuple[tuple[int, ...], np.array, int]]):
    session.add(Game(c=Config.c, n_simulations=Config.n_simulations))
    session.commit()
    game_id = session.execute(func.max(Game.id)).scalar()
    session.add_all(
        (Sample(state=state, policy=policy, outcome=bool(outcome), move=move, game_id=game_id) for
         move, (state, policy, outcome) in
         enumerate(buffer)
         )
    )
    session.commit()
