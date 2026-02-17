# Personal Resolution Tracker — Specification

## 1. Overview

A single-user personal resolution tracker that helps set, monitor, and achieve goals throughout the year. The app uses AI (AWS Bedrock — Claude Haiku 4.5) to categorize goals, prioritize them, analyze sentiment on progress updates, and provide feedback.

## 2. Tech Stack

| Layer      | Technology                                               |
|------------|----------------------------------------------------------|
| Backend    | Python 3.12+, FastAPI, uvicorn                           |
| Frontend   | React 18, TypeScript, Vite, shadcn/ui, Tailwind CSS      |
| Database   | SQLite (via `sqlite3` standard library)                  |
| AI         | AWS Bedrock — `claude-haiku-4-5-20251001` in `us-east-1` |
| HTTP Client| boto3 (Bedrock Runtime)                                  |

## 3. Data Model

### 3.1 `resolutions` table

| Column        | Type    | Description                                         |
|---------------|---------|-----------------------------------------------------|
| id            | INTEGER | Primary key, autoincrement                          |
| title         | TEXT    | Short name of the resolution                        |
| description   | TEXT    | Detailed, measurable goal statement                 |
| category      | TEXT    | AI-assigned category (e.g., Health, Finance, Learning, Career, Personal) |
| priority      | INTEGER | AI-assigned priority (1 = highest)                  |
| target_date   | TEXT    | ISO-8601 date for goal completion                   |
| status        | TEXT    | `active`, `completed`, `abandoned`                  |
| created_at    | TEXT    | ISO-8601 timestamp                                  |
| updated_at    | TEXT    | ISO-8601 timestamp                                  |

### 3.2 `check_ins` table

| Column         | Type    | Description                                               |
|----------------|---------|-----------------------------------------------------------|
| id             | INTEGER | Primary key, autoincrement                                |
| resolution_id  | INTEGER | FK → resolutions.id                                       |
| note           | TEXT    | User-provided progress update                             |
| sentiment      | TEXT    | AI-analyzed sentiment (`positive`, `neutral`, `negative`) |
| sentiment_score| REAL    | Confidence score 0.0–1.0                                  |
| ai_feedback    | TEXT    | AI-generated encouragement or advice                      |
| created_at     | TEXT    | ISO-8601 timestamp                                        |

### 3.3 `reminders` table

| Column         | Type    | Description                                         |
|----------------|---------|-----------------------------------------------------|
| id             | INTEGER | Primary key, autoincrement                          |
| resolution_id  | INTEGER | FK → resolutions.id                                 |
| frequency      | TEXT    | `daily`, `weekly`, `biweekly`, `monthly`            |
| next_due       | TEXT    | ISO-8601 date of next check-in                      |
| is_active      | INTEGER | 1 = active, 0 = paused                              |

## 4. Backend API (FastAPI)

Base path: `/api`

### 4.1 Resolutions

| Method | Endpoint               | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | `/resolutions`         | List all resolutions                |
| POST   | `/resolutions`         | Create a resolution (AI categorizes & prioritizes) |
| GET    | `/resolutions/{id}`    | Get resolution detail with check-ins|
| PUT    | `/resolutions/{id}`    | Update a resolution                 |
| DELETE | `/resolutions/{id}`    | Delete a resolution                 |

### 4.2 Check-ins

| Method | Endpoint                          | Description                              |
|--------|-----------------------------------|------------------------------------------|
| GET    | `/resolutions/{id}/check-ins`     | List check-ins for a resolution          |
| POST   | `/resolutions/{id}/check-ins`     | Submit a check-in (AI analyzes sentiment, generates feedback) |

### 4.3 Reminders

| Method | Endpoint                          | Description                                |
|--------|-----------------------------------|--------------------------------------------|
| GET    | `/reminders/due`                  | Get all reminders currently due            |
| PUT    | `/resolutions/{id}/reminder`      | Update reminder frequency for a resolution |

### 4.4 Dashboard

| Method | Endpoint               | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | `/dashboard/summary`   | Aggregated stats: completion %, sentiment trends, overdue reminders |

## 5. AI Integration (AWS Bedrock)

All AI calls go through a single `ai_service.py` module using `boto3` Bedrock Runtime `invoke_model`.

### 5.1 Categorize & Prioritize (on resolution create)
- Input: title + description of the new resolution, plus existing resolutions for context.
- Output: `{ "category": "...", "priority": N }`

### 5.2 Sentiment Analysis & Feedback (on check-in create)
- Input: the check-in note, plus resolution context (title, description, past check-ins).
- Output: `{ "sentiment": "positive|neutral|negative", "sentiment_score": 0.85, "ai_feedback": "..." }`

## 6. Frontend Pages

### 6.1 Dashboard (`/`)
- Summary cards: total resolutions, active, completed, average sentiment trend.
- Due reminders banner at top — highlights resolutions with overdue or due-today check-ins.
- Quick-add resolution form.

### 6.2 Resolution Detail (`/resolution/:id`)
- Resolution metadata (title, description, category, priority, target date, status).
- Check-in timeline: list of past check-ins with sentiment badges and AI feedback.
- Check-in form: text area to submit a new progress update.
- Reminder settings: dropdown to set check-in frequency.

### 6.3 Layout
- Responsive sidebar navigation (collapsible on mobile).
- Light/dark mode toggle.

## 7. In-App Reminders

- The `GET /reminders/due` endpoint returns resolutions needing a check-in.
- The frontend polls this endpoint on load (and every 5 minutes).
- Due reminders show as a dismissible banner on the dashboard and as badge indicators in the sidebar.
- When a check-in is submitted, the backend advances `next_due` based on the configured frequency.

## 8. Seed Data

On first launch, the app seeds the database with 5 example resolutions:

1. **Read 12 books this year** — Learning, measurable: 1 book/month.
2. **Run a half marathon** — Health, target date: October 2026.
3. **Save $10,000 in emergency fund** — Finance, measurable: ~$833/month.
4. **Learn conversational Korean** — Learning, target: hold a 10-min conversation by December.
5. **Meditate daily for 15 minutes** — Personal, measurable: daily streak tracking.

## 9. Directory Structure

```
week1/
├── backend/
│   ├── main.py              # FastAPI app, CORS, lifespan
│   ├── database.py          # SQLite init, connection helper
│   ├── models.py            # Pydantic models
│   ├── routers/
│   │   ├── resolutions.py   # Resolution CRUD endpoints
│   │   ├── check_ins.py     # Check-in endpoints
│   │   ├── reminders.py     # Reminder endpoints
│   │   └── dashboard.py     # Dashboard summary endpoint
│   ├── services/
│   │   ├── ai_service.py    # Bedrock integration
│   │   └── reminder_service.py  # Reminder logic
│   ├── seed.py              # Seed data loader
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── api/             # API client functions
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Dashboard, ResolutionDetail
│   │   └── lib/             # Utilities
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.ts
├── data/
│   └── resolutions.db       # SQLite database (gitignored)
└── SPECIFICATIONS.md        # This file
```

## 10. Development Workflow

```bash
# Backend
cd week1/backend
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd week1/frontend
npm install
npm run dev    # Vite dev server on port 5173, proxies /api to :8000
```

## 11. Non-Goals (out of scope for v1)

- User authentication / multi-user support.
- Email or push notifications.
- Mobile native app.
- Cloud deployment (runs locally only).
- Data export/import.
