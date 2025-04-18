"""
Goal schemas for request validation and response serialization.
"""
from marshmallow import Schema, fields, validates, ValidationError, post_load, validate
from app.schemas import BaseSchema
from app.utils.validators import validate_amount, validate_name, validate_date_format
from datetime import datetime, timedelta

class GoalSchema(BaseSchema):
    """Schema for goal model serialization."""
    user_id = fields.Integer(dump_only=True)
    name = fields.String()
    description = fields.String()
    target_amount = fields.Decimal(as_string=True, required=True)
    current_amount = fields.Decimal(as_string=True, dump_only=True)
    time_period = fields.TimeDelta(precision="days", required=True)
    end_date = fields.Date(dump_only=True)
    
    @validates('target_amount')
    def validate_target_amount(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)
    
    @validates('name')
    def validate_name_value(self, value):
        if value is not None:
            is_valid, message = validate_name(value, "Goal name")
            if not is_valid:
                raise ValidationError(message)

class GoalCreateSchema(Schema):
    """Schema for goal creation requests."""
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))
    target_amount = fields.Decimal(as_string=True, required=True)
    time_period_days = fields.Integer(required=True)
    
    @validates('target_amount')
    def validate_target_amount(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)
    
    @validates('time_period_days')
    def validate_time_period(self, value):
        if value <= 0:
            raise ValidationError("Time period must be greater than zero days")

class GoalUpdateSchema(Schema):
    """Schema for goal update requests."""
    name = fields.String(validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=500))
    target_amount = fields.Decimal(as_string=True)
    time_period_days = fields.Integer()
    
    @validates('target_amount')
    def validate_target_amount(self, value):
        if value is not None:
            is_valid, message, _ = validate_amount(value)
            if not is_valid:
                raise ValidationError(message)
    
    @validates('time_period_days')
    def validate_time_period(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Time period must be greater than zero days")

class GoalProgressSchema(Schema):
    """Schema for adding progress to a goal."""
    amount = fields.Decimal(as_string=True, required=True)
    wallet_id = fields.Integer(required=True)
    description = fields.String(validate=validate.Length(max=500))
    
    @validates('amount')
    def validate_amount_value(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)

class GoalResponseSchema(GoalSchema):
    """Schema for goal responses with additional stats."""
    progress_percentage = fields.Float(dump_only=True)
    remaining_amount = fields.Decimal(as_string=True, dump_only=True)
    days_remaining = fields.Integer(dump_only=True)
    daily_amount_needed = fields.Decimal(as_string=True, dump_only=True)
    
    @post_load
    def calculate_derived_fields(self, data, **kwargs):
        """Calculate derived fields after loading data."""
        if 'target_amount' in data and 'current_amount' in data:
            # Calculate progress percentage
            target = data['target_amount']
            current = data.get('current_amount', 0)
            
            if target > 0:
                data['progress_percentage'] = (current / target) * 100
            else:
                data['progress_percentage'] = 0
                
            # Calculate remaining amount
            data['remaining_amount'] = target - current
        
        if 'created_at' in data and 'time_period' in data:
            # Calculate end date and days remaining
            created_date = data['created_at'].date()
            end_date = created_date + data['time_period']
            today = datetime.now().date()
            
            data['end_date'] = end_date
            
            if end_date >= today:
                data['days_remaining'] = (end_date - today).days
                
                # Calculate daily amount needed
                if 'remaining_amount' in data and data['days_remaining'] > 0:
                    data['daily_amount_needed'] = data['remaining_amount'] / data['days_remaining']
                else:
                    data['daily_amount_needed'] = data['remaining_amount']
            else:
                data['days_remaining'] = 0
                data['daily_amount_needed'] = data['remaining_amount']
        
        return data