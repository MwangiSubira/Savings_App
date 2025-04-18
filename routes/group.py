from flask import Blueprint, request, jsonify
from app.services.group_service import GroupService
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('group', __name__)
group_service = GroupService()

@bp.route('', methods=['GET'])
@jwt_required()
def get_groups():
    user_id = get_jwt_identity()
    try:
        groups = group_service.get_user_groups(user_id)
        return jsonify([group.to_dict() for group in groups]), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve groups"}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_group():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Group name is required"}), 400
    
    try:
        group = group_service.create_group(
            name=data['name'],
            description=data.get('description'),
            created_by=user_id
        )
        
        return jsonify(group.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create group"}), 500

@bp.route('/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    user_id = get_jwt_identity()
    try:
        group, members = group_service.get_group_with_members(group_id, user_id)
        if group:
            result = group.to_dict()
            result['members'] = [
                {
                    'user_id': member.user_id,
                    'name': member.user.name if hasattr(member, 'user') else None,
                    'is_admin': member.is_admin,
                    'joined_at': member.joined_at.isoformat() if member.joined_at else None
                }
                for member in members
            ]
            return jsonify(result), 200
        return jsonify({"error": "Group not found or unauthorized"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve group"}), 500

@bp.route('/<int:group_id>', methods=['PUT'])
@jwt_required()
def update_group(group_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        group = group_service.update_group(
            group_id=group_id,
            user_id=user_id,
            name=data.get('name'),
            description=data.get('description')
        )
        
        if group:
            return jsonify(group.to_dict()), 200
        return jsonify({"error": "Group not found or unauthorized"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update group"}), 500

@bp.route('/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    user_id = get_jwt_identity()
    try:
        success = group_service.delete_group(group_id, user_id)
        if success:
            return jsonify({"message": "Group deleted successfully"}), 200
        return jsonify({"error": "Group not found or unauthorized"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete group"}), 500

@bp.route('/<int:group_id>/members', methods=['POST'])
@jwt_required()
def add_member(group_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'user_id' not in data:
        return jsonify({"error": "User ID is required"}), 400
    
    try:
        member = group_service.add_member(
            group_id=group_id,
            admin_user_id=user_id,
            user_id=data['user_id'],
            is_admin=data.get('is_admin', False)
        )
        
        if member:
            return jsonify(member.to_dict()), 201
        return jsonify({"error": "Failed to add member to group"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to add member to group"}), 500

@bp.route('/<int:group_id>/members/<int:member_id>', methods=['DELETE'])
@jwt_required()
def remove_member(group_id, member_id):
    user_id = get_jwt_identity()
    try:
        success = group_service.remove_member(
            group_id=group_id,
            admin_user_id=user_id,
            user_id=member_id
        )
        
        if success:
            return jsonify({"message": "Member removed successfully"}), 200
        return jsonify({"error": "Failed to remove member from group"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to remove member from group"}), 500

@bp.route('/<int:group_id>/leave', methods=['POST'])
@jwt_required()
def leave_group(group_id):
    user_id = get_jwt_identity()
    try:
        success = group_service.leave_group(group_id, user_id)
        if success:
            return jsonify({"message": "Left group successfully"}), 200
        return jsonify({"error": "Failed to leave group"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to leave group"}), 500