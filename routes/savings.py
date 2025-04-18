from flask import Blueprint, request, jsonify
from app.services.savings_service import SavingsService
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('savings', __name__)
savings_service = SavingsService()

@bp.route('', methods=['GET'])
@jwt_required()
def get_savings_updates():
    user_id = get_jwt_identity()
    try:
        # Add query params for filtering
        wallet_id = request.args.get('wallet_id', type=int)
        goal_id = request.args.get('goal_id', type=int)
        savings_type = request.args.get('type')
        
        savings_updates = savings_service.get_user_savings_updates(
            user_id=user_id,
            wallet_id=wallet_id,
            goal_id=goal_id,
            savings_type=savings_type
        )
        
        return jsonify([update.to_dict() for update in savings_updates]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve savings updates"}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_savings_update():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['wallet_id', 'amount', 'type']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Required fields: {', '.join(required_fields)}"}), 400
    
    try:
        savings_update = savings_service.create_savings_update(
            user_id=user_id,
            wallet_id=data['wallet_id'],
            amount=data['amount'],
            savings_type=data['type'],
            goal_id=data.get('goal_id'),
            description=data.get('description')
        )
        
        return jsonify(savings_update.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create savings update"}), 500

@bp.route('/<int:update_id>', methods=['GET'])
@jwt_required()
def get_savings_update(update_id):
    user_id = get_jwt_identity()
    try:
        update = savings_service.get_savings_update(update_id, user_id)
        if update:
            return jsonify(update.to_dict()), 200
        return jsonify({"error": "Savings update not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve savings update"}), 500

@bp.route('/<int:update_id>', methods=['PUT'])
@jwt_required()
def update_savings_update(update_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        update = savings_service.update_savings_update(
            update_id=update_id,
            user_id=user_id,
            description=data.get('description')
        )
        
        if update:
            return jsonify(update.to_dict()), 200
        return jsonify({"error": "Savings update not found or unauthorized"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update savings record"}), 500

@bp.route('/<int:update_id>', methods=['DELETE'])
@jwt_required()
def delete_savings_update(update_id):
    user_id = get_jwt_identity()
    try:
        success = savings_service.delete_savings_update(update_id, user_id)
        if success:
            return jsonify({"message": "Savings update deleted successfully"}), 200
        return jsonify({"error": "Savings update not found or unauthorized"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete savings update"}), 500

@bp.route('/summary', methods=['GET'])
@jwt_required()
def get_savings_summary():
    user_id = get_jwt_identity()
    try:
        summary = savings_service.get_user_savings_summary(user_id)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate savings summary"}), 500