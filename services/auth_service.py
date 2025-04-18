from app import db, jwt, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import current_app
import uuid

class AuthService:
    @property
    def verification_required(self):
        return current_app.config.get('EMAIL_VERIFICATION_ENABLED', True)
    
    def register_user(self, email, name, password):
        """Register a new user"""
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create new user
        user = User(email=email, name=name, password=password)
        
        db.session.add(user)
        db.session.commit()
        
        # In a real application, you would send a verification email here
        # if self.verification_required:
        #     self._send_verification_email(user)
        
        return user
    
    def login_user(self, email, password):
        """Authenticate a user and return tokens"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return None
        
        # Check if email verification is required
        if self.verification_required and not user.verified:
            raise ValueError("Email not verified. Please verify your email before logging in.")
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }
    
    def verify_email(self, token):
        """Verify user's email using token"""
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            return False
        
        user.verify()
        db.session.commit()
        
        return True
    
    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        return User.query.get(user_id)
    
    def get_user_by_email(self, email):
        """Get a user by email"""
        return User.query.filter_by(email=email).first()
    
    def initiate_password_reset(self, email):
        """Start the password reset process"""
        user = self.get_user_by_email(email)
        
        if not user:
            raise ValueError("Email not found")
        
        # Generate reset token
        reset_token = str(uuid.uuid4())
        
        # Store token in user model (consider using a separate table for this in production)
        user.verification_token = reset_token
        db.session.commit()
        
        # In a real app, send an email with the reset token
        # self._send_password_reset_email(user, reset_token)
        
        return True
    
    def complete_password_reset(self, token, new_password):
        """Complete the password reset process"""
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            return False
        
        # Validate password
        if len(new_password) < current_app.config.get('PASSWORD_MIN_LENGTH', 8):
            raise ValueError("Password is too short")
        
        # Update password
        user.set_password(new_password)
        user.verification_token = None
        db.session.commit()
        
        return True
    
    def change_password(self, user_id, current_password, new_password):
        """Change a user's password"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        # Verify current password
        if not user.check_password(current_password):
            return False
        
        # Validate new password
        if len(new_password) < current_app.config.get('PASSWORD_MIN_LENGTH', 8):
            raise ValueError("New password is too short")
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return True
    
    # Private methods
    def _send_verification_email(self, user):
        """Send verification email to user"""
        # This would be implemented with an email service
        pass
    
    def _send_password_reset_email(self, user, token):
        """Send password reset email to user"""
        # This would be implemented with an email service
        pass