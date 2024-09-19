from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    notes = relationship(
        "Notes", back_populates="owner", cascade="all, delete")
