from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.question import Question

from app.db import db
import enum


class DataType(enum.Enum):
    string = 1
    number = 2


parser = {
    'string': lambda x: x,
    'number': lambda x: float(x),
}


@dataclass
class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    value = db.Column(db.String)
    data_type = db.Column(db.Enum(DataType), nullable=False,
                          default=DataType.string)
    label = db.Column(db.String)
    question_id = db.Column(db.ForeignKey(Question.id))

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    question = relationship("Question", back_populates="options")

    def parse_value(self):
        return parser[self.data_type.name](self.value)
