from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Prediction
from app.schemas import LeaderboardEntry, PredictionOut

router = APIRouter(tags=["leaderboard"])


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def leaderboard(db: Session = Depends(get_db)):
    rows = (
        db.query(User.id, User.email, func.coalesce(func.sum(Prediction.points), 0).label("total_points"))
        .outerjoin(Prediction, Prediction.user_id == User.id)
        .group_by(User.id)
        .order_by(func.coalesce(func.sum(Prediction.points), 0).desc())
        .all()
    )
    return [LeaderboardEntry(user_id=r[0], email=r[1], total_points=r[2]) for r in rows]


@router.get("/users/{user_id}/predictions", response_model=List[PredictionOut])
def user_predictions(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()
