from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import Match, Prediction, User
from app.schemas import MatchOut, PredictionIn, PredictionOut

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("", response_model=List[MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.query(Match).order_by(Match.match_date).all()


@router.post("/predictions", response_model=PredictionOut)
def submit_prediction(
    payload: PredictionIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    match = db.query(Match).filter(Match.id == payload.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    if match.is_finished:
        raise HTTPException(status_code=400, detail="No puedes predecir un partido que ya tiene resultado")

    existing = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id, Prediction.match_id == match.id)
        .first()
    )
    if existing:
        existing.home_score_pred = payload.home_score_pred
        existing.away_score_pred = payload.away_score_pred
        db.commit()
        db.refresh(existing)
        return existing

    prediction = Prediction(
        user_id=current_user.id,
        match_id=match.id,
        home_score_pred=payload.home_score_pred,
        away_score_pred=payload.away_score_pred,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/predictions/me", response_model=List[PredictionOut])
def my_predictions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Prediction).filter(Prediction.user_id == current_user.id).all()
