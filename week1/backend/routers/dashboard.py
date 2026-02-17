from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..db_models import Resolution, CheckIn, Reminder
from ..models import DashboardSummary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    total = db.query(func.count(Resolution.id)).scalar()
    active = db.query(func.count(Resolution.id)).filter(Resolution.status == "active").scalar()
    completed = db.query(func.count(Resolution.id)).filter(Resolution.status == "completed").scalar()
    abandoned = db.query(func.count(Resolution.id)).filter(Resolution.status == "abandoned").scalar()

    total_check_ins = db.query(func.count(CheckIn.id)).scalar()

    avg_sentiment = db.query(func.avg(CheckIn.sentiment_score)).filter(CheckIn.sentiment_score.isnot(None)).scalar()
    if avg_sentiment is not None:
        avg_sentiment = round(avg_sentiment, 2)

    sentiment_rows = (
        db.query(CheckIn.sentiment, func.count(CheckIn.id))
        .filter(CheckIn.sentiment.isnot(None))
        .group_by(CheckIn.sentiment)
        .all()
    )
    sentiment_breakdown = {row[0]: row[1] for row in sentiment_rows}

    today = date.today().isoformat()
    overdue = (
        db.query(func.count(Reminder.id))
        .join(Resolution, Reminder.resolution_id == Resolution.id)
        .filter(Reminder.is_active == 1, Reminder.next_due <= today, Resolution.status == "active")
        .scalar()
    )

    return DashboardSummary(
        total_resolutions=total,
        active_resolutions=active,
        completed_resolutions=completed,
        abandoned_resolutions=abandoned,
        total_check_ins=total_check_ins,
        average_sentiment_score=avg_sentiment,
        overdue_reminders=overdue,
        sentiment_breakdown=sentiment_breakdown,
    )
