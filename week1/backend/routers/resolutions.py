from datetime import datetime, date, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, selectinload
from ..database import get_db
from ..db_models import Resolution, Reminder
from ..models import (
    ResolutionCreate,
    ResolutionUpdate,
    ResolutionResponse,
    ResolutionDetail,
    CheckInResponse,
    ReminderResponse,
)
from ..services.ai_service import categorize_and_prioritize

router = APIRouter(prefix="/api/resolutions", tags=["resolutions"])


@router.get("", response_model=list[ResolutionResponse])
def list_resolutions(db: Session = Depends(get_db)) -> list[ResolutionResponse]:
    rows = db.query(Resolution).order_by(Resolution.priority.asc(), Resolution.created_at.desc()).all()
    return [ResolutionResponse(**r._to_dict()) for r in rows]


@router.post("", response_model=ResolutionResponse, status_code=201)
def create_resolution(body: ResolutionCreate, db: Session = Depends(get_db)) -> ResolutionResponse:
    now = datetime.utcnow().isoformat()

    existing = db.query(Resolution.title, Resolution.category, Resolution.priority).all()
    existing_list = [{"title": r.title, "category": r.category, "priority": r.priority} for r in existing]

    ai_result = categorize_and_prioritize(body.title, body.description, existing_list)

    resolution = Resolution(
        title=body.title,
        description=body.description,
        category=ai_result["category"],
        priority=ai_result["priority"],
        target_date=body.target_date,
        status="active",
        created_at=now,
        updated_at=now,
    )
    db.add(resolution)
    db.flush()

    next_due = (date.today() + timedelta(weeks=1)).isoformat()
    reminder = Reminder(
        resolution_id=resolution.id,
        frequency="weekly",
        next_due=next_due,
        is_active=1,
    )
    db.add(reminder)
    db.commit()
    db.refresh(resolution)

    return ResolutionResponse(**resolution._to_dict())


@router.get("/{resolution_id}", response_model=ResolutionDetail)
def get_resolution(resolution_id: int, db: Session = Depends(get_db)) -> ResolutionDetail:
    resolution = (
        db.query(Resolution)
        .options(selectinload(Resolution.check_ins), selectinload(Resolution.reminder))
        .filter(Resolution.id == resolution_id)
        .first()
    )
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")

    return ResolutionDetail(
        **resolution._to_dict(),
        check_ins=[CheckInResponse(**c._to_dict()) for c in sorted(resolution.check_ins, key=lambda x: x.created_at, reverse=True)],
        reminder=ReminderResponse(**resolution.reminder._to_dict()) if resolution.reminder else None,
    )


@router.put("/{resolution_id}", response_model=ResolutionResponse)
def update_resolution(resolution_id: int, body: ResolutionUpdate, db: Session = Depends(get_db)) -> ResolutionResponse:
    resolution = db.query(Resolution).filter(Resolution.id == resolution_id).first()
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")

    updates = body.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    for key, value in updates.items():
        setattr(resolution, key, value)
    resolution.updated_at = datetime.utcnow().isoformat()

    db.commit()
    db.refresh(resolution)
    return ResolutionResponse(**resolution._to_dict())


@router.delete("/{resolution_id}", status_code=204)
def delete_resolution(resolution_id: int, db: Session = Depends(get_db)) -> None:
    resolution = db.query(Resolution).filter(Resolution.id == resolution_id).first()
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")
    db.delete(resolution)
    db.commit()
