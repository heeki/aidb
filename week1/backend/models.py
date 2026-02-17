from pydantic import BaseModel
from typing import Optional


# --- Resolutions ---

class ResolutionCreate(BaseModel):
    title: str
    description: str
    target_date: Optional[str] = None


class ResolutionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[str] = None
    status: Optional[str] = None


class ResolutionResponse(BaseModel):
    id: int
    title: str
    description: str
    category: Optional[str] = None
    priority: Optional[int] = None
    target_date: Optional[str] = None
    status: str
    created_at: str
    updated_at: str


class ResolutionDetail(ResolutionResponse):
    check_ins: list["CheckInResponse"] = []
    reminder: Optional["ReminderResponse"] = None


# --- Check-ins ---

class CheckInCreate(BaseModel):
    note: str


class CheckInResponse(BaseModel):
    id: int
    resolution_id: int
    note: str
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    ai_feedback: Optional[str] = None
    created_at: str


# --- Reminders ---

class ReminderUpdate(BaseModel):
    frequency: str
    is_active: Optional[bool] = True


class ReminderResponse(BaseModel):
    id: int
    resolution_id: int
    frequency: str
    next_due: str
    is_active: bool


class DueReminder(BaseModel):
    resolution_id: int
    resolution_title: str
    frequency: str
    next_due: str


# --- Dashboard ---

class DashboardSummary(BaseModel):
    total_resolutions: int
    active_resolutions: int
    completed_resolutions: int
    abandoned_resolutions: int
    total_check_ins: int
    average_sentiment_score: Optional[float] = None
    overdue_reminders: int
    sentiment_breakdown: dict[str, int] = {}
