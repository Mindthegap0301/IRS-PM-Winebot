from sqlalchemy import func
from sqlalchemy.orm import relationship

from dataclasses import dataclass
import enum
from app.models.user import User
from app.db import db


class Status(enum.Enum):
    start = 1
    in_progress = 2
    ready = 3
    complete = 4
    cancelled = 5


@dataclass
class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id), nullable=False, index=True)
    name = db.Column(db.String)
    end_time = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Enum(Status), nullable=False, default=Status.start)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    chats = relationship("Chat", back_populates="chat_session")
    results = relationship("Result", back_populates="chat_session")
