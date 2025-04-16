from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.order import Order
from models.order_items import OrderItem
from models.customer import Customer
from models.product import Product
from utils.db import db
import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
    Place an order.
    Expected JSON:
    {
      "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
      ]
    }
    """
    data = request.get_json()
    print(data)
    if not data or "items" not in data:
        return jsonify({"error": "No order items provided"}), 400
    items = data["items"]

    current_user_email = get_jwt_identity()
    customer = Customer.query.filter_by(email=current_user_email).first()
    if not customer:
        return jsonify({"error": "User not found"}), 404

    total_amount = 0
    order_items = []
    for item in items:
        product = Product.query.get(item["product_id"])
        if not product:
            return jsonify({"error": f"Product {item['product_id']} not found"}), 404
        if product.stock_quantity < item["quantity"]:
            return jsonify({"error": f"Insufficient stock for product {product.name}"}), 400

        total_amount += product.price * item["quantity"]
        order_item = OrderItem(
            quantity=item["quantity"],
            price=product.price,
            product_id=product.product_id
        )
        order_items.append(order_item)
        # Update product stock
        product.stock_quantity -= item["quantity"]

    new_order = Order(
        order_date=datetime.date.today(),
        total_amount=total_amount,
        status="Pending",
        customer_id=customer.customer_id,
        order_items=order_items
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order placed", "order_id": new_order.order_id}), 201

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Retrieve order history for the logged in user."""
    current_user_email = get_jwt_identity()
    customer = Customer.query.filter_by(email=current_user_email).first()
    if not customer:
        return jsonify({"error": "User not found"}), 404

    orders = Order.query.filter_by(customer_id=customer.customer_id).all()
    orders_data = []
    for order in orders:
        orders_data.append({
            "order_id": order.order_id,
            "order_date": order.order_date.isoformat(),
            "total_amount": order.total_amount,
            "status": order.status
        })
    return jsonify(orders_data), 200

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Retrieve a specific order for the logged in user."""
    current_user_email = get_jwt_identity()
    customer = Customer.query.filter_by(email=current_user_email).first()
    if not customer:
        return jsonify({"error": "User not found"}), 404

    order = Order.query.filter_by(order_id=order_id, customer_id=customer.customer_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order_items = []
    for item in order.order_items:
        order_items.append({
            "order_item_id": item.order_item_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        })

    order_data = {
        "order_id": order.order_id,
        "order_date": order.order_date.isoformat(),
        "total_amount": order.total_amount,
        "status": order.status,
        "order_items": order_items
    }
    return jsonify(order_data), 200
