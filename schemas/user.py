"""
User schemas for request validation and response serialization.
"""
from marshmallow import Schema, fields, validates, ValidationError, post_load, validate
from app.schemas import BaseSchema
from app.utils.validators import validate_email
import re

class UserSchema(BaseSchema):
    """Schema for user model serialization."""
    name = fields.String(required=True)
    email = fields.Email(required=True)
    verified = fields.Boolean(dump_only=True)
    is_admin = fields.Boolean(dump_only=True)
    
    @validates('email')
    def validate_email_format(self, value):
        is_valid, message = validate_email(value)
        if not is_valid:
            raise ValidationError(message)

class UserRegistrationSchema(Schema):
    """Schema for user registration requests."""
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.String(
        required=True, 
        validate=validate.Length(min=8),
        load_only=True
    )
    confirm_password = fields.String(
        required=True,
        load_only=True
    )
    
    @validates('email')
    def validate_email_format(self, value):
        is_valid, message = validate_email(value)
        if not is_valid:
            raise ValidationError(message)
    
    @validates('password')
    def validate_password_strength(self, value):
        # Check for at least one uppercase, one lowercase, one digit, one special char
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise ValidationError("Password must contain at least one special character")
    
    @validates('confirm_password')
    def validate_passwords_match(self, value, **kwargs):
        if value != kwargs['data'].get('password', ''):
            raise ValidationError("Passwords do not match")

class UserLoginSchema(Schema):
    """Schema for user login requests."""
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

class UserProfileUpdateSchema(Schema):
    """Schema for user profile updates."""
    name = fields.String(validate=validate.Length(min=1, max=100))
    
    # Additional optional profile fields could be added here
    phone = fields.String()
    profile_picture_url = fields.URL()
    currency_preference = fields.String(validate=validate.Length(equal=3))

class PasswordChangeSchema(Schema):
    """Schema for password change requests."""
    current_password = fields.String(required=True, load_only=True)
    new_password = fields.String(
        required=True, 
        validate=validate.Length(min=8),
        load_only=True
    )
    confirm_password = fields.String(
        required=True,
        load_only=True
    )
    
    @validates('new_password')
    def validate_password_strength(self, value):
        # Check for at least one uppercase, one lowercase, one digit, one special char
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise ValidationError("Password must contain at least one special character")
    
    @validates('confirm_password')
    def validate_passwords_match(self, value, **kwargs):
        if value != kwargs['data'].get('new_password', ''):
            raise ValidationError("Passwords do not match")

class PasswordResetRequestSchema(Schema):
    """Schema for password reset requests."""
    email = fields.Email(required=True)

class PasswordResetSchema(Schema):
    """Schema for completing password reset."""
    token = fields.String(required=True)
    new_password = fields.String(
        required=True, 
        validate=validate.Length(min=8),
        load_only=True
    )
    confirm_password = fields.String(
        required=True,
        load_only=True
    )
    
    @validates('new_password')
    def validate_password_strength(self, value):
        # Check for at least one uppercase, one lowercase, one digit, one special char
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain at least one number")
        if not re.search(r'[^A-Za-z0-9]', value):
            raise ValidationError("Password must contain at least one special character")
    
    @validates('confirm_password')
    def validate_passwords_match(self, value, **kwargs):
        if value != kwargs['data'].get('new_password', ''):
            raise ValidationError("Passwords do not match")

class UserResponseSchema(UserSchema):
    """Schema for user responses with additional fields."""
    wallet_count = fields.Integer(dump_only=True)
    goal_count = fields.Integer(dump_only=True)
    group_count = fields.Integer(dump_only=True)