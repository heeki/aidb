from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..db_models import Resolution, Reminder
from ..models import ReminderUpdate, ReminderResponse, DueReminder
from ..services.reminder_service import advance_next_due

router = APIRouter(tags=["reminders"])


@router.get("/api/reminders/due", response_model=list[DueReminder])
def get_due_reminders(db: Session = Depends(get_db)) -> list[DueReminder]:
    today = date.today().isoformat()
    rows = (
        db.query(Reminder, Resolution.title)
        .join(Resolution, Reminder.resolution_id == Resolution.id)
        .filter(Reminder.is_active == 1, Reminder.next_due <= today, Resolution.status == "active")
        .order_by(Reminder.next_due.asc())
        .all()
    )
    return [
        DueReminder(
            resolution_id=r.Reminder.resolution_id,
            resolution_title=r.title,
            frequency=r.Reminder.frequency,
            next_due=r.Reminder.next_due,
        )
        for r in rows
    ]


@router.put("/api/resolutions/{resolution_id}/reminder", response_model=ReminderResponse)
def update_reminder(resolution_id: int, body: ReminderUpdate, db: Session = Depends(get_db)) -> ReminderResponse:
    if body.frequency not in ("daily", "weekly", "biweekly", "monthly"):
        raise HTTPException(status_code=400, detail="Invalid frequency")

    resolution = db.query(Resolution).filter(Resolution.id == resolution_id).first()
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")

    reminder = db.query(Reminder).filter(Reminder.resolution_id == resolution_id).first()

    if reminder:
        new_due = advance_next_due(reminder.next_due, body.frequency)
        reminder.frequency = body.frequency
        reminder.next_due = new_due
        reminder.is_active = int(body.is_active)
    else:
        new_due = advance_next_due(date.today().isoformat(), body.frequency)
        reminder = Reminder(
            resolution_id=resolution_id,
            frequency=body.frequency,
            next_due=new_due,
            is_active=int(body.is_active),
        )
        db.add(reminder)

    db.commit()
    db.refresh(reminder)
    return ReminderResponse(**reminder._to_dict())
