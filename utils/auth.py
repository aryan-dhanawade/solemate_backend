from datetime import timedelta
from flask_jwt_extended import create_access_token, decode_token
from utils.db import bcrypt

def hash_password(password: str) -> str:
    """
    Hashes a password using Flask-Bcrypt.
    
    :param password: Plain text password.
    :return: Hashed password as a UTF-8 string.
    """
    # generate_password_hash returns a bytes object, so we decode it.
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against its hash.
    
    :param password: Plain text password.
    :param hashed_password: The hashed password.
    :return: True if match, else False.
    """
    return bcrypt.check_password_hash(hashed_password, password)

def create_jwt(identity: str, expires_in_minutes: int = 60) -> str:
    """
    Creates a JWT token for a given identity.
    
    :param identity: A unique identifier (e.g., user email or id).
    :param expires_in_minutes: Expiration time in minutes.
    :return: JWT token string.
    """
    expires_delta = timedelta(minutes=expires_in_minutes)
    return create_access_token(identity=identity, expires_delta=expires_delta)

def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token.
    
    :param token: JWT token string.
    :return: Decoded token payload.
    """
    try:
        return decode_token(token)
    except Exception as e:
        # In production, log this exception.
        return {"error": str(e)}
