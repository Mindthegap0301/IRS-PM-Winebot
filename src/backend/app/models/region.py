from dataclasses import dataclass
from app.db import db


@dataclass
class Region(db.Model):
    __tablename__ = "regions"
    no = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    country = db.Column(db.String)
    designation = db.Column(db.String)
    province = db.Column(db.String)
    region_1 = db.Column(db.String)
    region_2 = db.Column(db.String)
    winery = db.Column(db.String)
