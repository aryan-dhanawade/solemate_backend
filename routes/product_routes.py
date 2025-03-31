from flask import Blueprint, request, jsonify
from models.product import Product
from models.category import Category
from utils.db import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    """Retrieve all products with optional filtering."""
    products = Product.query.all()
    data = []
    for product in products:
        
        data.append({
            "product_id": product.product_id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "category_id": product.category.category_id if product.category else None,
            
            "category": product.category.name if product.category else None

        })
    return jsonify(data), 200

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Retrieve a single product by its ID."""
    product = Product.query.get_or_404(product_id)
    data = {
        "product_id": product.product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity,
        "category": product.category.name if product.category else None
    }
    return jsonify(data), 200

@product_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product (admin only).
    
    Expected JSON:
    {
      "name": "Air Max 90",
      "description": "Classic style sneakers",
      "price": 120.99,
      "stock_quantity": 50,
      "category_id": 1  // Optional
    }
    """
    data = request.get_json()
    required_fields = ["name", "price", "stock_quantity"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required product fields"}), 400

    new_product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=data["price"],
        stock_quantity=data["stock_quantity"],
        category_id=data.get("category_id")
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created", "product_id": new_product.product_id}), 201

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product (admin only)."""
    data = request.get_json()
    product = Product.query.get_or_404(product_id)

    product.name = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price = data.get("price", product.price)
    product.stock_quantity = data.get("stock_quantity", product.stock_quantity)
    product.category_id = data.get("category_id", product.category_id)
    db.session.commit()

    return jsonify({"message": "Product updated"}), 200

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product (admin only)."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
