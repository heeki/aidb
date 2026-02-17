from datetime import datetime, date, timedelta
from .database import get_session_factory
from .db_models import Resolution, Reminder

SEED_RESOLUTIONS = [
    {
        "title": "Read 12 books this year",
        "description": "Read one book per month across a mix of fiction and non-fiction to broaden knowledge and maintain a reading habit.",
        "category": "Learning",
        "priority": 2,
        "target_date": "2026-12-31",
    },
    {
        "title": "Run a half marathon",
        "description": "Train progressively to complete a half marathon (21.1 km) by October 2026, following a structured running plan.",
        "category": "Health",
        "priority": 1,
        "target_date": "2026-10-31",
    },
    {
        "title": "Save $10,000 in emergency fund",
        "description": "Save approximately $833 per month to build a $10,000 emergency fund by end of year.",
        "category": "Finance",
        "priority": 1,
        "target_date": "2026-12-31",
    },
    {
        "title": "Learn conversational Korean",
        "description": "Study Korean consistently to hold a 10-minute conversation with a native speaker by December 2026.",
        "category": "Learning",
        "priority": 3,
        "target_date": "2026-12-31",
    },
    {
        "title": "Meditate daily for 15 minutes",
        "description": "Build a daily meditation habit of 15 minutes to improve focus and reduce stress. Track daily streak.",
        "category": "Personal",
        "priority": 2,
        "target_date": "2026-12-31",
    },
]


def seed_if_empty() -> None:
    session = get_session_factory()()
    count = session.query(Resolution).count()
    if count > 0:
        session.close()
        return

    now = datetime.utcnow().isoformat()
    next_due = (date.today() + timedelta(weeks=1)).isoformat()

    for r in SEED_RESOLUTIONS:
        resolution = Resolution(
            title=r["title"],
            description=r["description"],
            category=r["category"],
            priority=r["priority"],
            target_date=r["target_date"],
            status="active",
            created_at=now,
            updated_at=now,
        )
        session.add(resolution)
        session.flush()

        reminder = Reminder(
            resolution_id=resolution.id,
            frequency="weekly",
            next_due=next_due,
            is_active=1,
        )
        session.add(reminder)

    session.commit()
    session.close()
