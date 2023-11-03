from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship


from app.db import db


@dataclass
class CipProgram(db.Model):
    __tablename__ = 'cip_programs'
    id = db.Column(db.String, primary_key=True)
    program_id = db.Column(db.ForeignKey('programs.id'))
    cip_id = db.Column(db.ForeignKey('cips.id'))

    cip = relationship('Cip', back_populates='cip_programs')
    program = relationship('Program', back_populates='cip_programs')

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())