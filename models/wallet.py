from app import db
from datetime import datetime
from decimal import Decimal

class Wallet(db.Model):
    __tablename__ = 'wallets'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False, default=0)
    name = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    savings_updates = db.relationship('SavingsUpdate', backref='wallet', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_id, amount=0, name=None):
        self.user_id = user_id
        self.amount = amount
        self.name = name
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.amount += Decimal(str(amount))
        return self.amount
    
    def withdraw(self, amount):
        amount_decimal = Decimal(str(amount))
        if amount_decimal <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount_decimal > self.amount:
            raise ValueError("Insufficient funds")
        self.amount -= amount_decimal
        return self.amount
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Wallet {self.id} - {self.amount}>'