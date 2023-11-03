from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.db import db

from app.models.cip_occupation import CipOccupation
from app.models.cip_program import CipProgram


@dataclass
class Cip(db.Model):
    __tablename__ = 'cips'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)

    # Educational programs
    cip_occupations = relationship('CipOccupation', back_populates='cip')
    cip_programs = relationship('CipProgram', back_populates='cip')

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())
