"""
Authentication utility functions for the savings app.
"""
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from functools import wraps
from flask import jsonify, request
import re
import hashlib
import secrets
import string
from app.models.user import User
from app import jwt

def admin_required(fn):
    """
    Decorator to require admin rights for an endpoint.
    Must be used with jwt_required.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_admin:
            return jsonify({"error": "Admin privileges required"}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def verified_required(fn):
    """
    Decorator to require email verification for an endpoint.
    Must be used with jwt_required.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.verified:
            return jsonify({"error": "Email verification required"}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def generate_verification_token():
    """Generate a secure token for email verification or password reset."""
    return secrets.token_urlsafe(32)

def hash_password(password):
    """
    Hash a password for storing.
    This is a utility function, but bcrypt from Flask-Bcrypt is used in the models.
    """
    salt = hashlib.sha256(secrets.token_bytes(16)).hexdigest()
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def generate_secure_password(length=12):
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_-+=<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def validate_password_strength(password):
    """
    Validate password strength.
    Returns (bool, str) tuple with status and message.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password meets strength requirements"

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "error": "Token has expired",
        "code": "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": "Invalid token",
        "code": "invalid_token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error": "Authorization token is missing",
        "code": "authorization_required"
    }), 401

def rate_limit_ip(ip_address, limit=100, period=60):
    """
    Basic rate limiting function. In a production app,
    you would use Redis or a similar tool for this.
    
    Args:
        ip_address: Client IP address
        limit: Maximum requests per period
        period: Time period in seconds
        
    Returns:
        bool: True if request is allowed, False if rate limited
    """
    # This is a placeholder - in a real app you'd implement rate limiting with Redis
    # For now, always return True (no rate limiting)
    return True

def get_token_from_request():
    """Extract JWT token from request headers or query parameters."""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split('Bearer ')[1]
    
    # Check for token in query parameters
    return request.args.get('token')