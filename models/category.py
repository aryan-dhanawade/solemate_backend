from utils.db import db

class Category(db.Model):
    __tablename__ = 'category'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Relationship: A category has many products.
    products = db.relationship('Product', backref='category', lazy=True)
