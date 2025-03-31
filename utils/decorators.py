from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.customer import Customer

def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_email = get_jwt_identity()


        user = Customer.query.filter_by(email=user_email).first()
        if user and user.is_admin:
            return function(*args, **kwargs)
        else:
            return jsonify({'error': 'This page is admin only'}), 403
    return wrapper

