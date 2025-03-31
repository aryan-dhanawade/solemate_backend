from utils.db import db

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    order_item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Foreign Keys: Links to Order & Product.
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id', ondelete='CASCADE'))
