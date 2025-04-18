"""
Savings schemas for request validation and response serialization.
"""
from marshmallow import Schema, fields, validates, ValidationError, post_load, validate
from app.schemas import BaseSchema
from app.utils.validators import validate_amount

class SavingsUpdateSchema(BaseSchema):
    """Schema for savings update model serialization."""
    user_id = fields.Integer(dump_only=True)
    wallet_id = fields.Integer(required=True)
    goal_id = fields.Integer()
    amount = fields.Decimal(as_string=True, required=True)
    type = fields.String(required=True, validate=validate.OneOf(['deposit', 'withdrawal', 'goal_progress']))
    description = fields.String()
    
    @validates('amount')
    def validate_amount_value(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)

class SavingsCreateSchema(Schema):
    """Schema for creating savings updates."""
    wallet_id = fields.Integer(required=True)
    goal_id = fields.Integer()
    amount = fields.Decimal(as_string=True, required=True)
    type = fields.String(required=True, validate=validate.OneOf(['deposit', 'withdrawal', 'goal_progress']))
    description = fields.String(validate=validate.Length(max=500))
    
    @validates('amount')
    def validate_amount_value(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)

class SavingsUpdateResponseSchema(SavingsUpdateSchema):
    """Schema for savings update responses with additional details."""
    wallet_name = fields.String(dump_only=True)
    goal_name = fields.String(dump_only=True)
    running_balance = fields.Decimal(as_string=True, dump_only=True)

class SavingsSummarySchema(Schema):
    """Schema for user savings summary."""
    total_savings = fields.Decimal(as_string=True)
    total_deposits = fields.Decimal(as_string=True)
    total_withdrawals = fields.Decimal(as_string=True)
    wallet_count = fields.Integer()
    goal_count = fields.Integer()
    goals_on_track = fields.Integer()
    monthly_savings_average = fields.Decimal(as_string=True)
    weekly_savings_average = fields.Decimal(as_string=True)
    
    # Monthly breakdown
    monthly_breakdown = fields.Dict(keys=fields.String(), values=fields.Decimal(as_string=True))
    
    # Wallet distribution
    wallet_distribution = fields.List(fields.Dict(keys=fields.String(), values=fields.Raw()))