from flask import Blueprint, request, jsonify
from models.payment import Payment
from models.order import Order
from utils.db import db
import datetime

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment', methods=['POST'])
def process_payment():
    """
    Process a payment for an order.
    Expected JSON:
    {
      "order_id": 1,
      "payment_method": "Credit Card",
      "amount": 99.99
    }
    """
    data = request.get_json()
    required_fields = ["order_id", "payment_method", "amount"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing payment details"}), 400

    order = Order.query.get(data["order_id"])
    if not order:
        return jsonify({"error": "Order not found"}), 404

    new_payment = Payment(
        amount=data["amount"],
        payment_date=datetime.date.today(),
        payment_method=data["payment_method"],
        order_id=order.order_id
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Payment processed", "payment_id": new_payment.payment_id}), 201

@payment_bp.route('/payment/<int:order_id>', methods=['GET'])
def get_payment(order_id):
    """Retrieve payment details for a specific order."""
    payment = Payment.query.filter_by(order_id=order_id).first()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment_data = {
        "payment_id": payment.payment_id,
        "amount": payment.amount,
        "payment_date": payment.payment_date.isoformat(),
        "payment_method": payment.payment_method
    }
    return jsonify(payment_data), 200
