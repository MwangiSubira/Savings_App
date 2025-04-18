"""
Wallet schemas for request validation and response serialization.
"""
from marshmallow import Schema, fields, validates, ValidationError, post_load, validate
from app.schemas import BaseSchema
from app.utils.validators import validate_amount, validate_name

class WalletSchema(BaseSchema):
    """Schema for wallet model serialization."""
    user_id = fields.Integer(dump_only=True)
    name = fields.String()
    amount = fields.Decimal(as_string=True, required=True)
    currency = fields.String(dump_only=True, default="USD")
    
    @validates('amount')
    def validate_amount_value(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)
    
    @validates('name')
    def validate_name_value(self, value):
        if value is not None:
            is_valid, message = validate_name(value, "Wallet name")
            if not is_valid:
                raise ValidationError(message)

class WalletCreateSchema(Schema):
    """Schema for wallet creation requests."""
    name = fields.String(validate=validate.Length(min=1, max=100))
    initial_amount = fields.Decimal(as_string=True, default=0)
    currency = fields.String(validate=validate.Length(equal=3), default="USD")
    
    @validates('initial_amount')
    def validate_initial_amount(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)

class WalletUpdateSchema(Schema):
    """Schema for wallet update requests."""
    name = fields.String(validate=validate.Length(min=1, max=100))

class WalletTransactionSchema(Schema):
    """Schema for wallet transactions (deposit/withdraw)."""
    amount = fields.Decimal(as_string=True, required=True)
    description = fields.String(validate=validate.Length(max=500))
    
    @validates('amount')
    def validate_amount_value(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)

class WalletDepositSchema(WalletTransactionSchema):
    """Schema for wallet deposit requests."""
    goal_id = fields.Integer()

class WalletWithdrawSchema(WalletTransactionSchema):
    """Schema for wallet withdrawal requests."""
    pass

class WalletTransferSchema(Schema):
    """Schema for transferring between wallets."""
    source_wallet_id = fields.Integer(required=True)
    destination_wallet_id = fields.Integer(required=True)
    amount = fields.Decimal(as_string=True, required=True)
    description = fields.String(validate=validate.Length(max=500))
    
    @validates('amount')
    def validate_amount_value(self, value):
        is_valid, message, _ = validate_amount(value)
        if not is_valid:
            raise ValidationError(message)
    
    @validates('source_wallet_id')
    def validate_source_wallet(self, value, **kwargs):
        if value == kwargs['data'].get('destination_wallet_id'):
            raise ValidationError("Source and destination wallets must be different")

class WalletResponseSchema(WalletSchema):
    """Schema for wallet responses with additional stats."""
    transaction_count = fields.Integer(dump_only=True)
    last_transaction_date = fields.DateTime(dump_only=True)
    highest_balance = fields.Decimal(dump_only=True, as_string=True)