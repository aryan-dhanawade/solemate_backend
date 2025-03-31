from flask import Blueprint, jsonify
from utils.decorators import admin_required
from utils.db import db

admin_bp = Blueprint('admin', __name__, template_folder='templates')

def serialize_model(model_instance):
    """Converts a SQLAlchemy model instance into a dict of its columns and values."""
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}

@admin_bp.route('/', methods=['GET'])
@admin_required  # Require admin authentication here.
def dashboard():
    from models.customer import Customer
    from models.order import Order
    from models.product import Product
    from models.contact import Contact
    from models.category import Category

    # Retrieve all customers and orders normally
    customers = [serialize_model(c) for c in Customer.query.all()]
    orders = [serialize_model(o) for o in Order.query.all()]

    # Explicit join query to fetch products along with their categories
    products_with_category = (
        db.session.query(Product, Category)
        .outerjoin(Category, Product.category_id == Category.category_id)
        .all()
    )

    # Serialize each product, adding the category name if available.
    def serialize_product_tuple(prod_cat_tuple):
        product, category = prod_cat_tuple
        data = serialize_model(product)
        data['category'] = category.name if category else None
        return data

    products = [serialize_product_tuple(item) for item in products_with_category]

    contacts = [serialize_model(c) for c in Contact.query.all()]

    data = {
        "customers": customers,
        "orders": orders,
        "products": products,
        "issues": contacts
    }

    return jsonify(data), 200
