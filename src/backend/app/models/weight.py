from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.question import Question

from app.db import db


@dataclass
class Weight(db.Model):
    __tablename__ = 'weights'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.ForeignKey(Question.id))
    weight_value = db.Column(db.Float)
    variable = db.Column(db.String)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    question = relationship("Question", back_populates="weights")
