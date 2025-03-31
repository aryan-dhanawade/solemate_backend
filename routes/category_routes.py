from flask import Blueprint, request, jsonify
from models.category import Category
from utils.db import db

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """Retrieve all product categories."""
    categories = Category.query.all()
    data = [{"category_id": cat.category_id, "name": cat.name} for cat in categories]
    return jsonify(data), 200

@category_bp.route('/categories', methods=['POST'])
def add_category():
    """Add a new product category.
    
    Expected JSON:
    {
      "name": "Sneakers"
    }
    """
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Category name is required"}), 400

    new_category = Category(name=data["name"])
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category created", "category_id": new_category.category_id}), 201
    