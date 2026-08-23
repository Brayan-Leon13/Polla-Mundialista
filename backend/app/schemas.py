from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models import Role


# ---------- Auth ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Matches ----------
class MatchOut(BaseModel):
    id: int
    group_id: int
    home_team: str
    away_team: str
    match_date: datetime
    home_score_real: Optional[int] = None
    away_score_real: Optional[int] = None

    class Config:
        from_attributes = True


class MatchResultIn(BaseModel):
    home_score_real: int
    away_score_real: int


# ---------- Predictions ----------
class PredictionIn(BaseModel):
    match_id: int
    home_score_pred: int
    away_score_pred: int


class PredictionOut(BaseModel):
    id: int
    match_id: int
    home_score_pred: int
    away_score_pred: int
    points: Optional[int] = None

    class Config:
        from_attributes = True


# ---------- Leaderboard ----------
class LeaderboardEntry(BaseModel):
    user_id: int
    email: EmailStr
    total_points: int
