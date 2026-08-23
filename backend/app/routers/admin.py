from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_admin
from app.database import get_db
from app.models import Match, Prediction
from app.schemas import MatchResultIn, MatchOut

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


def calculate_points(pred_home: int, pred_away: int, real_home: int, real_away: int) -> int:
    """Reglas: 3 pts acierto exacto, 1 pt acierto de ganador/empate, 0 pts fallo."""
    if pred_home == real_home and pred_away == real_away:
        return 3

    def outcome(h, a):
        if h > a:
            return "home"
        if h < a:
            return "away"
        return "draw"

    if outcome(pred_home, pred_away) == outcome(real_home, real_away):
        return 1
    return 0


@router.put("/matches/{match_id}/result", response_model=MatchOut)
def set_match_result(match_id: int, payload: MatchResultIn, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    match.home_score_real = payload.home_score_real
    match.away_score_real = payload.away_score_real
    db.commit()

    # Recalcular puntos de todas las predicciones de este partido
    predictions = db.query(Prediction).filter(Prediction.match_id == match.id).all()
    for pred in predictions:
        pred.points = calculate_points(
            pred.home_score_pred, pred.away_score_pred, match.home_score_real, match.away_score_real
        )
    db.commit()
    db.refresh(match)
    return match
