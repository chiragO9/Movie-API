from database import Base
from sqlalchemy import Column, Integer, String

class Movie(Base):
    __tablename__ = "movies"

    id       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title    = Column(String(100), nullable=False)
    director = Column(String(100), nullable=False)
    genre    = Column(String(50),  nullable=False)
    year     = Column(Integer,     nullable=False)