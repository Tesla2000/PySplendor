from sqlalchemy import Column, Boolean, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from db.Base import Base
from db.Game import Game


class Sample(Base):
    __tablename__ = 'Sample'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(ARRAY(Integer))
    policy = Column(ARRAY(Float))
    outcome = Column(Boolean)
    move = Column(Integer)
    game_id = Column(Integer, ForeignKey("Game.id", ondelete="CASCADE"))

    game = relationship(Game, back_populates="samples")

