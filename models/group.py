from app import db
from datetime import datetime

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_by = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = db.relationship('GroupMember', backref='group', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_groups')
    
    def __init__(self, name, description, created_by):
        self.name = name
        self.description = description
        self.created_by = created_by
    
    def add_member(self, user_id, is_admin=False):
        """Add a member to the group"""
        member = GroupMember(
            group_id=self.id,
            user_id=user_id,
            is_admin=is_admin
        )
        db.session.add(member)
        return member
    
    def remove_member(self, user_id):
        """Remove a member from the group"""
        member = GroupMember.query.filter_by(group_id=self.id, user_id=user_id).first()
        if member:
            db.session.delete(member)
            return True
        return False
    
    def is_member(self, user_id):
        """Check if a user is a member of the group"""
        return GroupMember.query.filter_by(group_id=self.id, user_id=user_id).first() is not None
    
    def is_admin(self, user_id):
        """Check if a user is an admin of the group"""
        member = GroupMember.query.filter_by(group_id=self.id, user_id=user_id).first()
        return member is not None and member.is_admin
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'member_count': len(self.members)
        }
    
    def __repr__(self):
        return f'<Group {self.name}>'

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    
    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(db.BigInteger, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, group_id, user_id, is_admin=False):
        self.group_id = group_id
        self.user_id = user_id
        self.is_admin = is_admin
    
    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'is_admin': self.is_admin,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }
    
    def __repr__(self):
        return f'<GroupMember group_id={self.group_id} user_id={self.user_id}>'