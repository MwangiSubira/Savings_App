"""
Serialization schemas for the savings app.
"""
from marshmallow import Schema, fields, validates, ValidationError, post_load
from datetime import datetime

class BaseSchema(Schema):
    """Base schema with common fields for all models."""
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    class Meta:
        ordered = True