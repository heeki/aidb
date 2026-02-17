from datetime import date, timedelta


def advance_next_due(current_due: str, frequency: str) -> str:
    due = date.fromisoformat(current_due)
    today = date.today()
    base = max(due, today)

    deltas = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
        "biweekly": timedelta(weeks=2),
        "monthly": timedelta(days=30),
    }
    delta = deltas.get(frequency, timedelta(weeks=1))
    return (base + delta).isoformat()
