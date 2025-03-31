from utils.db import db

class Customer(db.Model):
    __tablename__ = 'customer'
    
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationship: A customer has many orders.
    orders = db.relationship('Order', backref='customer', lazy=True)
