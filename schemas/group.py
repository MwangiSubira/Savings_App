"""
Group schemas for request validation and response serialization.
"""
from marshmallow import Schema, fields, validates, ValidationError, post_load, validate
from app.schemas import BaseSchema
from app.utils.validators import validate_name

class GroupSchema(BaseSchema):
    """Schema for group model serialization."""
    name = fields.String(required=True)
    description = fields.String()
    created_by = fields.Integer(dump_only=True)
    member_count = fields.Integer(dump_only=True)
    
    @validates('name')
    def validate_name_value(self, value):
        is_valid, message = validate_name(value, "Group name")
        if not is_valid:
            raise ValidationError(message)

class GroupCreateSchema(Schema):
    """Schema for group creation requests."""
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))

class GroupUpdateSchema(Schema):
    """Schema for group update requests."""
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))

class GroupMemberSchema(Schema):
    """Schema for group membership."""
    user_id = fields.Integer(dump_only=True)
    group_id = fields.Integer(dump_only=True)
    is_admin = fields.Boolean(default=False)
    joined_at = fields.DateTime(dump_only=True)
    name = fields.String(dump_only=True)  # User's name

class AddGroupMemberSchema(Schema):
    """Schema for adding a member to a group."""
    user_id = fields.Integer(required=True)
    is_admin = fields.Boolean(default=False)

class GroupResponseSchema(GroupSchema):
    """Schema for group responses with additional details."""
    members = fields.List(fields.Nested(GroupMemberSchema), dump_only=True)
    total_savings = fields.Decimal(as_string=True, dump_only=True)
    goals = fields.List(fields.Dict(), dump_only=True)  # Simplified goals list