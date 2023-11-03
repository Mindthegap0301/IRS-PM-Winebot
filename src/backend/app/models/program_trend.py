from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.program import Program


from app.db import db


@dataclass
class ProgramTrend(db.Model):
    __tablename__ = 'program_trends'
    id = db.Column(db.String, primary_key=True, index=True)
    year = db.Column(db.Integer, nullable=False)
    program_id = db.Column(db.ForeignKey(Program.id), nullable=False)

    employment_rate_overall = db.Column(db.Float)
    employment_rate_ft_perm = db.Column(db.Float)
    basic_monthly_mean = db.Column(db.Float)
    basic_monthly_median = db.Column(db.Float)
    gross_monthly_mean = db.Column(db.Float)
    gross_monthly_median = db.Column(db.Float)
    gross_mthly_25_percentile = db.Column(db.Float)
    gross_mthly_75_percentile = db.Column(db.Float)

    program = relationship("Program", back_populates="program_trends")

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())
