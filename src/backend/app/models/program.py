from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.db import db

from app.models.cip_program import CipProgram


@dataclass
class Program(db.Model):
    __tablename__ = "programs"
    id = db.Column(db.Integer, primary_key=True, index=True)
    university = db.Column(db.String)
    school = db.Column(db.String)
    degree = db.Column(db.String)

    program_trends = relationship("ProgramTrend", back_populates="program")
    cip_programs = relationship("CipProgram", back_populates="program")

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
