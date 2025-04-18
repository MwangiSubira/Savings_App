from app import db, bcrypt
import uuid
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    wallets = db.relationship('Wallet', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    savings_updates = db.relationship('SavingsUpdate', backref='user', lazy=True, cascade='all, delete-orphan')
    group_memberships = db.relationship('GroupMember', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.verified = False
        self.verification_token = str(uuid.uuid4())
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def generate_verification_token(self):
        self.verification_token = str(uuid.uuid4())
        return self.verification_token
    
    def verify(self):
        self.verified = True
        self.verification_token = None
        
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'verified': self.verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'