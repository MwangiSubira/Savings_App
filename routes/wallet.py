from flask import Blueprint, request, jsonify
from app.services.wallet_service import WalletService
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('wallet', __name__)
wallet_service = WalletService()

@bp.route('', methods=['GET'])
@jwt_required()
def get_wallets():
    user_id = get_jwt_identity()
    try:
        wallets = wallet_service.get_user_wallets(user_id)
        return jsonify([wallet.to_dict() for wallet in wallets]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve wallets"}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_wallet():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        wallet = wallet_service.create_wallet(
            user_id=user_id,
            name=data.get('name'),
            initial_amount=data.get('amount', 0)
        )
        return jsonify(wallet.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create wallet"}), 500

@bp.route('/<int:wallet_id>', methods=['GET'])
@jwt_required()
def get_wallet(wallet_id):
    user_id = get_jwt_identity()
    try:
        wallet = wallet_service.get_wallet(wallet_id, user_id)
        if wallet:
            return jsonify(wallet.to_dict()), 200
        return jsonify({"error": "Wallet not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve wallet"}), 500

@bp.route('/<int:wallet_id>', methods=['PUT'])
@jwt_required()
def update_wallet(wallet_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        wallet = wallet_service.update_wallet(
            wallet_id=wallet_id,
            user_id=user_id,
            name=data.get('name')
        )
        
        if wallet:
            return jsonify(wallet.to_dict()), 200
        return jsonify({"error": "Wallet not found or unauthorized"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update wallet"}), 500

@bp.route('/<int:wallet_id>', methods=['DELETE'])
@jwt_required()
def delete_wallet(wallet_id):
    user_id = get_jwt_identity()
    try:
        success = wallet_service.delete_wallet(wallet_id, user_id)
        if success:
            return jsonify({"message": "Wallet deleted successfully"}), 200
        return jsonify({"error": "Wallet not found or unauthorized"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete wallet"}), 500

@bp.route('/<int:wallet_id>/deposit', methods=['POST'])
@jwt_required()
def deposit(wallet_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400
    
    try:
        wallet, savings_update = wallet_service.deposit(
            wallet_id=wallet_id,
            user_id=user_id,
            amount=data['amount'],
            goal_id=data.get('goal_id'),
            description=data.get('description')
        )
        
        return jsonify({
            "wallet": wallet.to_dict(),
            "savings_update": savings_update.to_dict() if savings_update else None
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to process deposit"}), 500

@bp.route('/<int:wallet_id>/withdraw', methods=['POST'])
@jwt_required()
def withdraw(wallet_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400
    
    try:
        wallet, savings_update = wallet_service.withdraw(
            wallet_id=wallet_id,
            user_id=user_id,
            amount=data['amount'],
            description=data.get('description')
        )
        
        return jsonify({
            "wallet": wallet.to_dict(),
            "savings_update": savings_update.to_dict() if savings_update else None
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to process withdrawal"}), 500

@bp.route('/<int:wallet_id>/history', methods=['GET'])
@jwt_required()
def get_wallet_history(wallet_id):
    user_id = get_jwt_identity()
    try:
        history = wallet_service.get_wallet_history(wallet_id, user_id)
        return jsonify([entry.to_dict() for entry in history]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to retrieve wallet history"}), 500