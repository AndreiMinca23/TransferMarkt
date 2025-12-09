# backend/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    ForeignKey,
    func,
    DateTime,
)
from sqlalchemy.orm import relationship

from .db import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    competitions = relationship("Competition", back_populates="country")


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    country = relationship("Country", back_populates="competitions")
    clubs = relationship("Club", back_populates="competition")


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    players = relationship("Player", back_populates="position")


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    competition_id = Column(Integer, ForeignKey("competitions.id"))

    country = relationship("Country")
    competition = relationship("Competition", back_populates="clubs")
    players = relationship("Player", back_populates="current_club")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    nationality = Column(String(50), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"))
    current_club_id = Column(Integer, ForeignKey("clubs.id"))
    market_value = Column(Numeric(12, 2))

    position = relationship("Position", back_populates="players")
    current_club = relationship("Club", back_populates="players")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
