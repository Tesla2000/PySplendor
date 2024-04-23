from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import ARRAY

from db.Base import Base


class SpeedSample(Base):
    __tablename__ = 'SpeedSample'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(ARRAY(Integer))
    turns_till_end = Column(Integer)
    move_index = Column(Integer)

