from utils.db import db

class Product(db.Model):
    __tablename__ = 'product'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    
    # Foreign Key: Links to Category.
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='SET NULL'))
    
    # Relationship: A product has many order items.
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
