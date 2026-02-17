from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .seed import seed_if_empty
from .routers import resolutions, check_ins, reminders, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    seed_if_empty()
    yield


app = FastAPI(title="Resolution Tracker", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resolutions.router)
app.include_router(check_ins.router)
app.include_router(reminders.router)
app.include_router(dashboard.router)
