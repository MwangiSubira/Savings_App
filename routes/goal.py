from flask import Blueprint, request, jsonify
from app.services.goal_service import GoalService
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta

bp = Blueprint('goal', __name__)
goal_service = GoalService()

@bp.route('', methods=['GET'])
@jwt_required()
def get_goals():
    user_id = get_jwt_identity()
    try:
        goals = goal_service.get_user_goals(user_id)
        return jsonify([goal.to_dict() for goal in goals]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve goals"}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_goal():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'target_amount' not in data or 'time_period_days' not in data:
        return jsonify({"error": "Target amount and time period are required"}), 400
    
    try:
        # Convert days to interval
        time_period = timedelta(days=int(data['time_period_days']))
        
        goal = goal_service.create_goal(
            user_id=user_id,
            target_amount=data['target_amount'],
            time_period=time_period,
            description=data.get('description'),
            name=data.get('name')
        )
        
        return jsonify(goal.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create goal"}), 500

@bp.route('/<int:goal_id>', methods=['GET'])
@jwt_required()
def get_goal(goal_id):
    user_id = get_jwt_identity()
    try:
        goal = goal_service.get_goal(goal_id, user_id)
        if goal:
            return jsonify(goal.to_dict()), 200
        return jsonify({"error": "Goal not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve goal"}), 500

@bp.route('/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Convert days to interval if provided
        time_period = None
        if 'time_period_days' in data:
            time_period = timedelta(days=int(data['time_period_days']))
        
        goal = goal_service.update_goal(
            goal_id=goal_id,
            user_id=user_id,
            target_amount=data.get('target_amount'),
            time_period=time_period,
            description=data.get('description'),
            name=data.get('name')
        )
        
        if goal:
            return jsonify(goal.to_dict()), 200
        return jsonify({"error": "Goal not found or unauthorized"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update goal"}), 500

@bp.route('/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    user_id = get_jwt_identity()
    try:
        success = goal_service.delete_goal(goal_id, user_id)
        if success:
            return jsonify({"message": "Goal deleted successfully"}), 200
        return jsonify({"error": "Goal not found or unauthorized"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete goal"}), 500

@bp.route('/<int:goal_id>/progress', methods=['POST'])
@jwt_required()
def add_progress(goal_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'amount' not in data or 'wallet_id' not in data:
        return jsonify({"error": "Amount and wallet ID are required"}), 400
    
    try:
        result = goal_service.add_progress(
            goal_id=goal_id,
            user_id=user_id,
            amount=data['amount'],
            wallet_id=data['wallet_id'],
            description=data.get('description')
        )
        
        if result:
            goal, wallet, savings_update = result
            return jsonify({
                "goal": goal.to_dict(),
                "wallet": wallet.to_dict(),
                "savings_update": savings_update.to_dict()
            }), 200
        
        return jsonify({"error": "Failed to add progress"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to add progress to goal"}), 500

@bp.route('/<int:goal_id>/history', methods=['GET'])
@jwt_required()
def get_goal_history(goal_id):
    user_id = get_jwt_identity()
    try:
        history = goal_service.get_goal_history(goal_id, user_id)
        return jsonify([entry.to_dict() for entry in history]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to retrieve goal history"}), 500