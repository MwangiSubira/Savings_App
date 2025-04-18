from app import db
from app.models.group import Group, GroupMember
from app.models.user import User
from sqlalchemy.exc import IntegrityError

class GroupService:
    def get_user_groups(self, user_id):
        """Get all groups a user is a member of"""
        # Query through group members to find all groups
        memberships = GroupMember.query.filter_by(user_id=user_id).all()
        group_ids = [membership.group_id for membership in memberships]
        
        if not group_ids:
            return []
        
        return Group.query.filter(Group.id.in_(group_ids)).all()
    
    def create_group(self, name, created_by, description=None):
        """Create a new group"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Group name is required")
        
        # Create the group
        group = Group(
            name=name,
            description=description,
            created_by=created_by
        )
        
        db.session.add(group)
        db.session.commit()
        
        # Add creator as admin member
        member = GroupMember(
            group_id=group.id,
            user_id=created_by,
            is_admin=True
        )
        
        db.session.add(member)
        db.session.commit()
        
        return group
    
    def get_group(self, group_id, user_id):
        """Get a specific group if user is a member"""
        # Check if user is a member
        membership = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not membership:
            return None
        
        return Group.query.get(group_id)
    
    def get_group_with_members(self, group_id, user_id):
        """Get a group and its members if user is a member"""
        # First check if user is a member
        group = self.get_group(group_id, user_id)
        
        if not group:
            return None, None
        
        # Get all members with joined user data
        members = GroupMember.query.filter_by(group_id=group_id).all()
        
        # Load user data for each member
        for member in members:
            member.user = User.query.get(member.user_id)
        
        return group, members
    
    def update_group(self, group_id, user_id, name=None, description=None):
        """Update a group's details if user is an admin"""
        # Check if user is an admin
        membership = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id,
            is_admin=True
        ).first()
        
        if not membership:
            return None
        
        group = Group.query.get(group_id)
        
        if name is not None:
            if not name or len(name.strip()) == 0:
                raise ValueError("Group name cannot be empty")
            group.name = name
        
        if description is not None:
            group.description = description
        
        db.session.commit()
        return group
    
    def delete_group(self, group_id, user_id):
        """Delete a group if user is the creator or an admin"""
        # Check if user is an admin
        membership = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id,
            is_admin=True
        ).first()
        
        if not membership:
            return False
        
        group = Group.query.get(group_id)
        
        # Additional check for creator (optional - you might want only creators to delete)
        # if group.created_by != user_id:
        #     return False
        
        # Delete all members first
        GroupMember.query.filter_by(group_id=group_id).delete()
        
        # Then delete the group
        db.session.delete(group)
        db.session.commit()
        
        return True
    
    def add_member(self, group_id, admin_user_id, user_id, is_admin=False):
        """Add a new member to the group"""
        # Check if the adding user is an admin
        admin_membership = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=admin_user_id,
            is_admin=True
        ).first()
        
        if not admin_membership:
            raise ValueError("Only group admins can add members")
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check if user is already a member
        existing_member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if existing_member:
            raise ValueError("User is already a member of this group")
        
        # Add the new member
        member = GroupMember(
            group_id=group_id,
            user_id=user_id,
            is_admin=is_admin
        )
        
        db.session.add(member)
        db.session.commit()
        
        return member
    
    def remove_member(self, group_id, admin_user_id, user_id):
        """Remove a member from the group"""
        # Check if the removing user is an admin
        admin_membership = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=admin_user_id,
            is_admin=True
        ).first()
        
        if not admin_membership:
            raise ValueError("Only group admins can remove members")
        
        # Check if target user is a member
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not member:
            return False
        
        # Prevent removing the last admin
        if member.is_admin:
            # Check if this is the last admin
            admin_count = GroupMember.query.filter_by(
                group_id=group_id,
                is_admin=True
            ).count()
            
            if admin_count <= 1:
                raise ValueError("Cannot remove the last admin from the group")
        
        db.session.delete(member)
        db.session.commit()
        
        return True
    
    def update_member(self, group_id, admin_user_id, user_id, is_admin):
        """Update a member's admin status"""
        # Check if the updating user is an admin
        admin_membership = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=admin_user_id,
            is_admin=True
        ).first()
        
        if not admin_membership:
            raise ValueError("Only group admins can update members")
        
        # Check if target user is a member
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not member:
            return None
        
        # If removing admin status, check that this isn't the last admin
        if member.is_admin and not is_admin:
            # Check if this is the last admin
            admin_count = GroupMember.query.filter_by(
                group_id=group_id,
                is_admin=True
            ).count()
            
            if admin_count <= 1:
                raise ValueError("Cannot remove the last admin from the group")
        
        member.is_admin = is_admin
        db.session.commit()
        
        return member
    
    def leave_group(self, group_id, user_id):
        """Leave a group"""
        # Check if user is a member
        member = GroupMember.query.filter_by(
            group_id=group_id,
            user_id=user_id
        ).first()
        
        if not member:
            return False
        
        # Check if this is the last admin
        if member.is_admin:
            admin_count = GroupMember.query.filter_by(
                group_id=group_id,
                is_admin=True
            ).count()
            
            if admin_count <= 1:
                # Check if there are other members who could become admin
                member_count = GroupMember.query.filter_by(group_id=group_id).count()
                
                if member_count > 1:
                    raise ValueError("You are the last admin. Promote another member to admin before leaving.")
                else:
                    # User is the last member, delete the group
                    group = Group.query.get(group_id)
                    db.session.delete(group)
                    db.session.commit()
                    return True
        
        # User can leave
        db.session.delete(member)
        db.session.commit()
        
        return True