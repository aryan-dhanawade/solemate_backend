from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth import hash_password, verify_password, create_jwt
from models.customer import Customer
from utils.db import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new customer.
    Expected JSON:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890",
        "address": "123 Main St",
        "password": "plaintextpassword"
    }
    """
    data = request.get_json()

    # Validate required fields
    required_fields = ["name", "email", "phone", "address", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    address = data["address"]
    password = data["password"]

    # Check if user already exists by email or phone
    existing_customer = Customer.query.filter(
        (Customer.email == email) | (Customer.phone == phone)
    ).first()
    if existing_customer:
        return jsonify({"error": "User with that email or phone already exists"}), 400

    # Hash the password and create a new customer
    hashed = hash_password(password)
    new_customer = Customer(
        name=name,
        email=email,
        phone=phone,
        address=address,
        password=hashed
    )
    db.session.add(new_customer)
    db.session.commit()
    token = create_jwt(identity=new_customer.email)

    return jsonify({"message": "User registered successfully", "access_token": token, "user": {
            "customer_id": new_customer.customer_id,
            "name": new_customer.name,
            "email": new_customer.email,
            "phone": new_customer.phone,
            "address": new_customer.address,
        } }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a customer.
    Expected JSON:
    {
        "email": "john@example.com",
        "password": "plaintextpassword"
    }
    """
    data = request.get_json()

    # Validate required fields
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data["email"]
    password = data["password"]

    # Look up customer by email
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"error": "User not found"}), 404

    # Verify password
    if not verify_password(password, customer.password):
        return jsonify({"error": "Incorrect password"}), 401

    # Create a JWT token with the customer's email as identity
    token = create_jwt(identity=customer.email)
    return jsonify({"message": "Login successful", "access_token": token, "is_admin": customer.is_admin, "user": {
        "email": customer.email,
        "name": customer.name
    } }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Returns the profile of the currently authenticated customer.
    """
    current_user_email = get_jwt_identity()
    customer = Customer.query.filter_by(email=current_user_email).first()

    if not customer:
        return jsonify({"error": "User not found"}), 404

    # Return profile details (exclude sensitive info such as password)
    return jsonify({
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address,
        "is_admin": customer.is_admin
    }), 200


@auth_bp.route("/subscribe", methods=["POST"])
@jwt_required()
def subscribe_to_newsletter():

    """Subscribes the user with the email to the newsletter"""
    data = request.get_json()
    user_email = data["email"]
    customer = Customer.query.filter_by(email=user_email).first()

    if not customer:
        return jsonify({"error": "User not found"}), 404
    
    customer.newsletter = True
    db.session.commit()


    return jsonify({"message": "Subscribed", "email": user_email}), 200
