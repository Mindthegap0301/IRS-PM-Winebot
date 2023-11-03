from sqlalchemy import func
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from app.db import db

# from app.models.cip_occupation import CipOccupation


@dataclass
class Occupation(db.Model):
    __tablename__ = 'occupations'
    id = db.Column(db.String, primary_key=True, index=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    job_zone = db.Column(db.Integer)
    task = db.Column(db.Text)
    index = db.Column(db.Integer)

    education_mode = db.Column(db.Integer)
    education_median = db.Column(db.Integer)
    # Experience
    experience_mode = db.Column(db.Integer)
    experience_median = db.Column(db.Integer)

    # Style
    cons_fre = db.Column(db.Float)
    role_wine = db.Column(db.Float)
    life_style = db.Column(db.Float)
    wine_taste = db.Column(db.Float)
    reputation = db.Column(db.Float)
    # Context
    per_week = db.Column(db.Float)
    new_wine = db.Column(db.Float)
    friend_gather = db.Column(db.Float)
    visit_winery = db.Column(db.Float)

    # Salary
    min_salary = db.Column(db.Float)
    max_salary = db.Column(db.Float)

    ssoc_jobs = relationship("SsocJob", back_populates="occupation")

    # Educational programs
    cip_occupations = relationship(
        'CipOccupation', back_populates='occupation')

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())
