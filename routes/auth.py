from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.validators import validate_registration, validate_login
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('auth', __name__)
auth_service = AuthService()

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    validation_errors = validate_registration(data)
    if validation_errors:
        return jsonify({"errors": validation_errors}), 400
    
    try:
        user = auth_service.register_user(
            email=data['email'],
            name=data['name'],
            password=data['password']
        )
        return jsonify({
            "message": "Registration successful",
            "user": user.to_dict(),
            "verification_required": auth_service.verification_required
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Registration failed"}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    validation_errors = validate_login(data)
    if validation_errors:
        return jsonify({"errors": validation_errors}), 400
    
    try:
        token_data = auth_service.login_user(
            email=data['email'],
            password=data['password']
        )
        
        if not token_data:
            return jsonify({"error": "Invalid credentials"}), 401
            
        return jsonify(token_data), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Login failed"}), 500

@bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    
    if not data or 'token' not in data:
        return jsonify({"error": "Verification token is required"}), 400
    
    try:
        result = auth_service.verify_email(data['token'])
        if result:
            return jsonify({"message": "Email verified successfully"}), 200
        else:
            return jsonify({"error": "Invalid verification token"}), 400
    except Exception as e:
        return jsonify({"error": "Verification failed"}), 500

@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
    
    try:
        auth_service.initiate_password_reset(data['email'])
        return jsonify({"message": "Password reset instructions sent to email"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Password reset failed"}), 500

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    
    if not data or 'token' not in data or 'password' not in data:
        return jsonify({"error": "Token and new password are required"}), 400
    
    try:
        result = auth_service.complete_password_reset(data['token'], data['password'])
        if result:
            return jsonify({"message": "Password reset successful"}), 200
        else:
            return jsonify({"error": "Invalid or expired reset token"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Password reset failed"}), 500

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    try:
        user = auth_service.get_user_by_id(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve user information"}), 500

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({"error": "Current password and new password are required"}), 400
    
    try:
        result = auth_service.change_password(
            user_id, 
            data['current_password'], 
            data['new_password']
        )
        
        if result:
            return jsonify({"message": "Password changed successfully"}), 200
        else:
            return jsonify({"error": "Current password is incorrect"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Password change failed"}), 500