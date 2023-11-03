from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.occupation import Occupation

from app.db import db


@dataclass
class SsocJob(db.Model):
    __tablename__ = 'ssoc_jobs'
    id = db.Column(db.String, primary_key=True, index=True, nullable=False)
    occupation_id = db.Column(db.ForeignKey(Occupation.id), nullable=False)
    ssoc_code = db.Column(db.String)
    ssoc_job_title = db.Column(db.String)
    isco_code = db.Column(db.String)
    min_salary = db.Column(db.Float)
    max_salary = db.Column(db.Float)

    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now())

    occupation = relationship("Occupation")
