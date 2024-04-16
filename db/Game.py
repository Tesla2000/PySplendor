from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

from .Base import Base


class Game(Base):
    __tablename__ = 'Game'

    id = Column(Integer, primary_key=True, autoincrement=True)
    c = Column(Float)
    n_simulations = Column(Integer)
    samples = relationship("Sample", back_populates="game", cascade="all, delete-orphan")
