from app import db
from datetime import datetime
from decimal import Decimal

class SavingsUpdate(db.Model):
    __tablename__ = 'savings_updates'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    wallet_id = db.Column(db.BigInteger, db.ForeignKey('wallets.id'), nullable=False)
    goal_id = db.Column(db.BigInteger, db.ForeignKey('goals.id'), nullable=True)
    amount = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False)  # deposit, withdrawal
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_id, wallet_id, amount, type, goal_id=None, description=None):
        self.user_id = user_id
        self.wallet_id = wallet_id
        self.goal_id = goal_id
        self.amount = Decimal(str(amount))
        self.description = description
        self.type = type
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'wallet_id': self.wallet_id,
            'goal_id': self.goal_id,
            'amount': float(self.amount),
            'description': self.description,
            'type': self.type,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SavingsUpdate {self.id} - {self.type} {self.amount}>'