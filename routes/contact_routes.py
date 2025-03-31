from flask import Blueprint, request, jsonify
from models.contact import Contact
from utils.db import db

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=['POST'])
def send_request():
    """
    Contact Us Route
    Expected JSON:
    {
        "name": "XYZ", 
        "email": "xyz@gmail.com", 
        "subject": "issue raised for ABC product", 
        "message": "issue details"
    }
    """
    data = request.get_json()
    required_fields = ["name", "email", "subject", "message"]
    
    # Validate required fields
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        new_contact = Contact(
            name=data["name"],
            email=data["email"],
            subject=data["subject"],
            message=data["message"]
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({"message": "Your request has been submitted successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
