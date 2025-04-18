from app import db
from datetime import datetime
from decimal import Decimal

class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    target_amount = db.Column(db.Numeric, nullable=False)
    current_amount = db.Column(db.Numeric, nullable=False, default=0)
    time_period = db.Column(db.Interval, nullable=False)  # Using PostgreSQL's interval type
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    achieved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    savings_updates = db.relationship('SavingsUpdate', backref='goal', lazy=True)
    
    def __init__(self, user_id, target_amount, time_period, description=None, name=None):
        self.user_id = user_id
        self.target_amount = Decimal(str(target_amount))
        self.current_amount = Decimal('0')
        self.time_period = time_period
        self.description = description
        self.name = name
        self.start_date = datetime.utcnow()
        self.end_date = self.start_date + time_period if time_period else None
        self.achieved = False
    
    def add_progress(self, amount):
        """Add progress to the goal and check if it's achieved"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        self.current_amount += Decimal(str(amount))
        
        if self.current_amount >= self.target_amount:
            self.achieved = True
            
        return self.current_amount
    
    @property
    def progress_percentage(self):
        """Calculate the percentage of goal completion"""
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100
    
    @property
    def is_expired(self):
        """Check if the goal has expired"""
        if not self.end_date:
            return False
        return datetime.utcnow() > self.end_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining until goal expiration"""
        if not self.end_date:
            return None
        
        remaining = self.end_date - datetime.utcnow()
        return max(0, remaining.days)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_amount': float(self.target_amount),
            'current_amount': float(self.current_amount),
            'progress_percentage': float(self.progress_percentage),
            'time_period_days': self.time_period.days if self.time_period else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'days_remaining': self.days_remaining,
            'description': self.description,
            'name': self.name,
            'achieved': self.achieved,
            'is_expired': self.is_expired,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Goal {self.id} - {self.current_amount}/{self.target_amount}>'