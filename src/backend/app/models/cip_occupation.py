from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.db import db


@dataclass
class CipOccupation(db.Model):
    __tablename__ = 'cip_occupations'
    id = db.Column(db.String, primary_key=True)
    occupation_id = db.Column(db.ForeignKey('occupations.id'))
    cip_id = db.Column(db.ForeignKey('cips.id'))

    cip = relationship('Cip', back_populates='cip_occupations')
    occupation = relationship('Occupation', back_populates='cip_occupations')

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())
