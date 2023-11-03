from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.db import db


@dataclass
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    group = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    text = db.Column(db.Text, nullable=False)
    min_response_length = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    options = relationship("Option", back_populates="question")
    weights = relationship("Weight", back_populates="question")

    def get_options_dict(self):
        if self.options:
            return list(map(lambda option: {'id': option.id, 'order': option.order, 'value': option.value, 'data_type': option.data_type.name, 'label': option.label}, self.options))
