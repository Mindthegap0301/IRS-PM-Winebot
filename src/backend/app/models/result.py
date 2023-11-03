from sqlalchemy import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship

from app.models.product import Product
from app.models.chat_session import ChatSession

from app.db import db


@dataclass
class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True, index=True)
    product_id = db.Column(db.ForeignKey(Product.id))
    description_similarity = db.Column(db.Float)
    taste_exp_similarity = db.Column(db.Float)
    variety_similarity = db.Column(db.Float)
    pairing_similarity = db.Column(db.Float)
    price_similarity = db.Column(db.Float)
    score = db.Column(db.Float)

    user_rating = db.Column(db.Integer)

    chat_session_id = db.Column(db.ForeignKey(ChatSession.id))

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    chat_session = relationship("ChatSession", back_populates="results")
    product = relationship("Product")
