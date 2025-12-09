from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


# ============================================================
#                    COUNTRY / COMPETITION / CLUB / POSITION
# ============================================================


class CountryBase(BaseModel):
  id: int
  name: str

  class Config:
      from_attributes = True


class CompetitionBase(BaseModel):
  id: int
  name: str
  country_id: int

  class Config:
      from_attributes = True


class ClubBase(BaseModel):
  id: int
  name: str
  country_id: Optional[int] = None
  competition_id: Optional[int] = None

  class Config:
      from_attributes = True


class PositionBase(BaseModel):
  id: int
  name: str

  class Config:
      from_attributes = True


# ============================================================
#                          PLAYER
# ============================================================


class PlayerBase(BaseModel):
  id: int
  name: str
  birth_date: Optional[date] = None
  nationality: Optional[str] = None
  position_id: Optional[int] = None
  current_club_id: Optional[int] = None
  market_value: Optional[Decimal] = None

  class Config:
      from_attributes = True


# ============================================================
#                          USER
# ============================================================


class UserBase(BaseModel):
  full_name: str
  email: EmailStr
  phone: constr(strip_whitespace=True, min_length=6, max_length=20)  # type: ignore[valid-type]


class UserCreate(UserBase):
  password: constr(min_length=6)  # type: ignore[valid-type]


class UserOut(UserBase):
  id: int
  created_at: datetime

  class Config:
      from_attributes = True


# ============================================================
#                       AUTH / LOGIN
# ============================================================


class LoginRequest(BaseModel):
  email: EmailStr
  password: str


class RegisterRequest(UserCreate):
  """Folosit la /api/register – aceleași câmpuri ca UserCreate."""
  pass


class LoginResponse(BaseModel):
  access_token: str
  user: UserOut


# ============================================================
#                       SEARCH SCHEMAS
# ============================================================


class PlayerDetails(BaseModel):
  id: int
  name: str
  birth_date: Optional[date] = None
  nationality: Optional[str] = None
  position_name: Optional[str] = None
  club_name: Optional[str] = None
  market_value: Optional[Decimal] = None

  class Config:
      from_attributes = True


class ClubShort(BaseModel):
  id: int
  name: str

  class Config:
      from_attributes = True


class SearchClubResponse(BaseModel):
  type: str = "club"
  club: ClubShort
  players: list[PlayerDetails]


class SearchPlayerResponse(BaseModel):
  type: str = "player"
  player: PlayerDetails

class ClubDetails(BaseModel):
    id: int
    name: str
    country_name: Optional[str] = None
    competition_name: Optional[str] = None

    class Config:
        from_attributes = True