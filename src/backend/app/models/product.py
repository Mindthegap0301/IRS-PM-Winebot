from sqlalchemy import func
from sqlalchemy.orm import relationship
from dataclasses import dataclass
from app.db import db


@dataclass
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.String, primary_key=True, index=True, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    product_price = db.Column(db.String, nullable=False)
    product_link = db.Column(db.String, nullable=False)
    product_desc = db.Column(
        db.String,
    )
    expert_review = db.Column(db.String)
    customer_review = db.Column(db.String)
    apperance = db.Column(db.String)
    nose = db.Column(db.String)
    food_pair = db.Column(db.String)
    alcohol_percent = db.Column(db.String)
    bottle_size = db.Column(db.String)
    have_gift_box = db.Column(db.String)
    oringin = db.Column(db.String)
    varietal = db.Column(db.String)
    brand = db.Column(db.String)
    alcohol_type = db.Column(db.String)
    varietals = db.Column(db.String)
    organic = db.Column(db.String)
    vintage = db.Column(db.String)
    style = db.Column(db.String)
    score = db.Column(db.String)
    finish = db.Column(db.String)
    type = db.Column(db.String)
    palate = db.Column(db.String)
    taste_description = db.Column(db.String)
    food_pair_description = db.Column(db.String)
    varietal_description = db.Column(db.String)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
