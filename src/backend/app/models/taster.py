from dataclasses import dataclass
from app.db import db


@dataclass
class Taster(db.Model):
    __tablename__ = "taster"
    no = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    point = db.Column(db.String)
    taster_name = db.Column(db.String)
    taster_twitter = db.Column(db.String)
