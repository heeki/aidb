from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Resolution(Base):
    __tablename__ = "resolutions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Text)
    priority = Column(Integer)
    target_date = Column(Text)
    status = Column(Text, nullable=False, default="active")
    created_at = Column(Text, nullable=False)
    updated_at = Column(Text, nullable=False)

    check_ins = relationship("CheckIn", back_populates="resolution", cascade="all, delete-orphan")
    reminder = relationship("Reminder", back_populates="resolution", uselist=False, cascade="all, delete-orphan")

    def _to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "target_date": self.target_date,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class CheckIn(Base):
    __tablename__ = "check_ins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False)
    note = Column(Text, nullable=False)
    sentiment = Column(Text)
    sentiment_score = Column(Float)
    ai_feedback = Column(Text)
    created_at = Column(Text, nullable=False)

    resolution = relationship("Resolution", back_populates="check_ins")

    def _to_dict(self) -> dict:
        return {
            "id": self.id,
            "resolution_id": self.resolution_id,
            "note": self.note,
            "sentiment": self.sentiment,
            "sentiment_score": self.sentiment_score,
            "ai_feedback": self.ai_feedback,
            "created_at": self.created_at,
        }


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resolution_id = Column(Integer, ForeignKey("resolutions.id", ondelete="CASCADE"), nullable=False, unique=True)
    frequency = Column(Text, nullable=False, default="weekly")
    next_due = Column(Text, nullable=False)
    is_active = Column(Integer, nullable=False, default=1)

    resolution = relationship("Resolution", back_populates="reminder")

    def _to_dict(self) -> dict:
        return {
            "id": self.id,
            "resolution_id": self.resolution_id,
            "frequency": self.frequency,
            "next_due": self.next_due,
            "is_active": self.is_active,
        }
