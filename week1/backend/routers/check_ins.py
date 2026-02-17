from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..db_models import Resolution, CheckIn, Reminder
from ..models import CheckInCreate, CheckInResponse
from ..services.ai_service import analyze_sentiment_and_feedback
from ..services.reminder_service import advance_next_due

router = APIRouter(prefix="/api/resolutions/{resolution_id}/check-ins", tags=["check-ins"])


@router.get("", response_model=list[CheckInResponse])
def list_check_ins(resolution_id: int, db: Session = Depends(get_db)) -> list[CheckInResponse]:
    resolution = db.query(Resolution).filter(Resolution.id == resolution_id).first()
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")

    rows = (
        db.query(CheckIn)
        .filter(CheckIn.resolution_id == resolution_id)
        .order_by(CheckIn.created_at.desc())
        .all()
    )
    return [CheckInResponse(**r._to_dict()) for r in rows]


@router.post("", response_model=CheckInResponse, status_code=201)
def create_check_in(resolution_id: int, body: CheckInCreate, db: Session = Depends(get_db)) -> CheckInResponse:
    resolution = db.query(Resolution).filter(Resolution.id == resolution_id).first()
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")

    past = (
        db.query(CheckIn.note, CheckIn.sentiment, CheckIn.created_at)
        .filter(CheckIn.resolution_id == resolution_id)
        .order_by(CheckIn.created_at.desc())
        .limit(5)
        .all()
    )
    past_list = [{"note": r.note, "sentiment": r.sentiment, "created_at": r.created_at} for r in past]

    ai_result = analyze_sentiment_and_feedback(
        note=body.note,
        resolution_title=resolution.title,
        resolution_description=resolution.description,
        past_check_ins=past_list,
    )

    now = datetime.utcnow().isoformat()
    check_in = CheckIn(
        resolution_id=resolution_id,
        note=body.note,
        sentiment=ai_result["sentiment"],
        sentiment_score=ai_result["sentiment_score"],
        ai_feedback=ai_result["ai_feedback"],
        created_at=now,
    )
    db.add(check_in)

    reminder = (
        db.query(Reminder)
        .filter(Reminder.resolution_id == resolution_id, Reminder.is_active == 1)
        .first()
    )
    if reminder:
        new_due = advance_next_due(reminder.next_due, reminder.frequency)
        reminder.next_due = new_due

    db.commit()
    db.refresh(check_in)
    return CheckInResponse(**check_in._to_dict())
