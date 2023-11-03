from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.occupation import Occupation

from app.db import db


@dataclass
class CareerPath(db.Model):
    __tablename__ = 'career_paths'
    id = db.Column(db.String, primary_key=True, index=True, nullable=False)
    source_id = db.Column(db.ForeignKey(Occupation.id), nullable=False)
    target_id = db.Column(db.ForeignKey(Occupation.id), nullable=False)
    difference = db.Column(db.Float)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    source = relationship(Occupation, foreign_keys=[
                          source_id])
    target = relationship(Occupation, foreign_keys=[
                          target_id])
