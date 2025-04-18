"""
Input validation utilities for the savings app.
"""
import re
from decimal import Decimal, InvalidOperation
from datetime import datetime
import uuid

def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        tuple: (is_valid, message)
    """
    if not email:
        return False, "Email is required"
        
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        return False, "Invalid email format"
        
    return True, "Valid email"

def validate_amount(amount):
    """
    Validate that an amount is a valid decimal > 0.
    
    Args:
        amount: Amount to validate
        
    Returns:
        tuple: (is_valid, message, converted_amount)
    """
    if amount is None:
        return False, "Amount is required", None
    
    # Convert to Decimal if not already
    try:
        decimal_amount = Decimal(str(amount)) if not isinstance(amount, Decimal) else amount
    except (InvalidOperation, ValueError, TypeError):
        return False, "Amount must be a valid number", None
    
    if decimal_amount <= 0:
        return False, "Amount must be greater than zero", None
    
    # Restrict to 2 decimal places
    decimal_amount = decimal_amount.quantize(Decimal('0.01'))
    
    return True, "Valid amount", decimal_amount

def validate_name(name, field_name="Name", min_length=1, max_length=100):
    """
    Validate a name field (user name, wallet name, etc.)
    
    Args:
        name: Name to validate
        field_name: Field name for error messages
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        tuple: (is_valid, message)
    """
    if name is None:
        return False, f"{field_name} is required"
    
    name_str = str(name).strip()
    
    if len(name_str) < min_length:
        return False, f"{field_name} must be at least {min_length} characters"
        
    if len(name_str) > max_length:
        return False, f"{field_name} cannot exceed {max_length} characters"
    
    return True, f"Valid {field_name.lower()}"

def validate_date_format(date_str, format="%Y-%m-%d"):
    """
    Validate that a string is a valid date in the specified format.
    
    Args:
        date_str: Date string to validate
        format: Expected date format
        
    Returns:
        tuple: (is_valid, message, date_obj)
    """
    if not date_str:
        return False, "Date is required", None
    
    try:
        date_obj = datetime.strptime(date_str, format)
        return True, "Valid date", date_obj
    except ValueError:
        return False, f"Invalid date format. Expected format: {format}", None

def validate_date_range(start_date, end_date):
    """
    Validate that end_date is after start_date.
    
    Args:
        start_date: Start date (datetime object)
        end_date: End date (datetime object)
        
    Returns:
        tuple: (is_valid, message)
    """
    if not start_date or not end_date:
        return False, "Both start and end dates are required"
    
    if end_date <= start_date:
        return False, "End date must be after start date"
    
    return True, "Valid date range"

def validate_uuid(uuid_str):
    """
    Validate that a string is a valid UUID.
    
    Args:
        uuid_str: UUID string to validate
        
    Returns:
        tuple: (is_valid, message, uuid_obj)
    """
    if not uuid_str:
        return False, "UUID is required", None
    
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return True, "Valid UUID", uuid_obj
    except ValueError:
        return False, "Invalid UUID format", None

def validate_currency_code(currency_code):
    """
    Validate that a string is a valid ISO 4217 currency code.
    This is a simplified version - a real implementation would have a complete list.
    
    Args:
        currency_code: Currency code to validate
        
    Returns:
        tuple: (is_valid, message)
    """
    common_currencies = {
        'USD', 'EUR', 'JPY', 'GBP', 'CAD', 'AUD', 'CHF', 'CNY', 'INR', 'BRL', 
        'RUB', 'KRW', 'SGD', 'NZD', 'MXN', 'HKD', 'NOK', 'SEK', 'ZAR', 'TRY'
    }
    
    if not currency_code:
        return False, "Currency code is required"
    
    code = currency_code.upper()
    
    if len(code) != 3:
        return False, "Currency code must be 3 characters"
    
    if not code.isalpha():
        return False, "Currency code must contain only letters"
    
    if code not in common_currencies:
        return False, "Unrecognized currency code"
    
    return True, "Valid currency code"

def validate_description(description, max_length=500):
    """
    Validate a description field.
    
    Args:
        description: Description to validate
        max_length: Maximum allowed length
        
    Returns:
        tuple: (is_valid, message)
    """
    if description is None:
        return True, "Description is optional"
    
    description_str = str(description).strip()
    
    if len(description_str) > max_length:
        return False, f"Description cannot exceed {max_length} characters"
    
    return True, "Valid description"

def validate_phone_number(phone):
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        tuple: (is_valid, message)
    """
    if not phone:
        return True, "Phone number is optional"
    
    # Remove any non-digit characters
    clean_phone = re.sub(r'\D', '', phone)
    
    # Check length (7-15 digits is generally valid internationally)
    if len(clean_phone) < 7 or len(clean_phone) > 15:
        return False, "Phone number must be between 7 and 15 digits"
    
    return True, "Valid phone number"