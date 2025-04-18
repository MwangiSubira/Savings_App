from app import db
from app.models.savings import SavingsUpdate
from app.models.wallet import Wallet
from app.models.goal import Goal
from decimal import Decimal
from sqlalchemy import func, desc
from datetime import datetime, timedelta

class SavingsService:
    def get_user_savings_updates(self, user_id, wallet_id=None, goal_id=None, savings_type=None):
        """Get savings updates for a user with optional filters"""
        query = SavingsUpdate.query.filter_by(user_id=user_id)
        
        if wallet_id:
            query = query.filter_by(wallet_id=wallet_id)
        
        if goal_id:
            query = query.filter_by(goal_id=goal_id)
        
        if savings_type:
            query = query.filter_by(type=savings_type)
        
        return query.order_by(SavingsUpdate.updated_at.desc()).all()
    
    def get_savings_update(self, update_id, user_id):
        """Get a specific savings update"""
        return SavingsUpdate.query.filter_by(id=update_id, user_id=user_id).first()
    
    def create_savings_update(self, user_id, wallet_id, amount, savings_type, goal_id=None, description=None):
        """Create a new savings update record"""
        # Validate amount
        if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        
        # Verify wallet exists and belongs to user
        wallet = Wallet.query.filter_by(id=wallet_id, user_id=user_id).first()
        if not wallet:
            raise ValueError("Wallet not found or unauthorized")
        
        # If goal_id provided, verify it exists and belongs to user
        if goal_id:
            goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
            if not goal:
                raise ValueError("Goal not found or unauthorized")
        
        # Validate savings_type
        valid_types = ['deposit', 'withdrawal', 'goal_contribution', 'transfer']
        if savings_type not in valid_types:
            raise ValueError(f"Invalid savings type. Must be one of: {', '.join(valid_types)}")
        
        # Update wallet balance based on type
        if savings_type == 'deposit':
            wallet.deposit(amount)
        elif savings_type in ['withdrawal', 'goal_contribution']:
            if wallet.amount < Decimal(str(amount)):
                raise ValueError("Insufficient funds in wallet")
            wallet.withdraw(amount)
        
        # Update goal amount if applicable
        if goal_id and savings_type == 'goal_contribution':
            goal = Goal.query.get(goal_id)
            goal.add_progress(amount)
        
        # Create savings update record
        savings_update = SavingsUpdate(
            user_id=user_id,
            wallet_id=wallet_id,
            goal_id=goal_id,
            amount=amount,
            type=savings_type,
            description=description
        )
        
        db.session.add(savings_update)
        db.session.commit()
        
        return savings_update
    
    def update_savings_update(self, update_id, user_id, description=None):
        """Update a savings update record (only description can be modified)"""
        update = self.get_savings_update(update_id, user_id)
        
        if not update:
            return None
        
        if description is not None:
            update.description = description
        
        db.session.commit()
        return update
    
    def delete_savings_update(self, update_id, user_id):
        """Delete a savings update record"""
        update = self.get_savings_update(update_id, user_id)
        
        if not update:
            return False
        
        # This operation is complex as it needs to revert the associated changes
        # in wallet and potentially goal balances
        
        # Get the affected wallet
        wallet = Wallet.query.get(update.wallet_id)
        
        # Reverse the original transaction effect
        if update.type == 'deposit':
            # Check if wallet has sufficient funds to remove deposit
            if wallet.amount < update.amount:
                raise ValueError("Cannot delete deposit as wallet has insufficient funds")
            wallet.withdraw(update.amount)
        elif update.type in ['withdrawal', 'goal_contribution']:
            wallet.deposit(update.amount)
        
        # If a goal was involved, reverse that too
        if update.goal_id and update.type == 'goal_contribution':
            goal = Goal.query.get(update.goal_id)
            
            # Ensure goal exists and has sufficient funds
            if goal and goal.current_amount >= update.amount:
                goal.current_amount -= update.amount
        
        db.session.delete(update)
        db.session.commit()
        
        return True
    
    def get_user_savings_summary(self, user_id):
        """Generate a summary of the user's savings activity"""
        # Get total deposits
        total_deposits = db.session.query(func.sum(SavingsUpdate.amount))\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'deposit')\
            .scalar() or 0
        
        # Get total withdrawals
        total_withdrawals = db.session.query(func.sum(SavingsUpdate.amount))\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'withdrawal')\
            .scalar() or 0
        
        # Get total goal contributions
        total_goal_contributions = db.session.query(func.sum(SavingsUpdate.amount))\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'goal_contribution')\
            .scalar() or 0
        
        # Get current wallet balance
        current_balance = db.session.query(func.sum(Wallet.amount))\
            .filter(Wallet.user_id == user_id)\
            .scalar() or 0
        
        # Get recent transactions
        recent_transactions = SavingsUpdate.query\
            .filter(SavingsUpdate.user_id == user_id)\
            .order_by(SavingsUpdate.updated_at.desc())\
            .limit(5)\
            .all()
        
        # Get monthly savings data (last 6 months)
        today = datetime.now()
        six_months_ago = today - timedelta(days=180)
        
        monthly_data = []
        current_date = six_months_ago
        
        while current_date <= today:
            month_start = datetime(current_date.year, current_date.month, 1)
            
            if current_date.month == 12:
                month_end = datetime(current_date.year + 1, 1, 1)
            else:
                month_end = datetime(current_date.year, current_date.month + 1, 1)
            
            # Get deposits for this month
            month_deposits = db.session.query(func.sum(SavingsUpdate.amount))\
                .filter(
                    SavingsUpdate.user_id == user_id,
                    SavingsUpdate.type == 'deposit',
                    SavingsUpdate.created_at >= month_start,
                    SavingsUpdate.created_at < month_end
                ).scalar() or 0
            
            # Get withdrawals for this month
            month_withdrawals = db.session.query(func.sum(SavingsUpdate.amount))\
                .filter(
                    SavingsUpdate.user_id == user_id,
                    SavingsUpdate.type == 'withdrawal',
                    SavingsUpdate.created_at >= month_start,
                    SavingsUpdate.created_at < month_end
                ).scalar() or 0
            
            monthly_data.append({
                'month': month_start.strftime('%Y-%m'),
                'deposits': float(month_deposits),
                'withdrawals': float(month_withdrawals),
                'net': float(month_deposits - month_withdrawals)
            })
            
            # Move to next month
            if current_date.month == 12:
                current_date = datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime(current_date.year, current_date.month + 1, 1)
        
        return {
            'total_deposits': float(total_deposits),
            'total_withdrawals': float(total_withdrawals),
            'total_goal_contributions': float(total_goal_contributions),
            'current_balance': float(current_balance),
            'net_savings': float(total_deposits - total_withdrawals),
            'recent_transactions': [t.to_dict() for t in recent_transactions],
            'monthly_data': monthly_data
        }
    
    def get_savings_statistics(self, user_id, period=None):
        """Generate savings statistics for a user with optional time filter"""
        # Define time period filter
        if period:
            today = datetime.now()
            if period == 'week':
                start_date = today - timedelta(days=7)
            elif period == 'month':
                start_date = today - timedelta(days=30)
            elif period == 'year':
                start_date = today - timedelta(days=365)
            else:
                start_date = None
        else:
            start_date = None
        
        # Base query for deposits
        deposits_query = db.session.query(SavingsUpdate)\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'deposit')
            
        # Base query for withdrawals
        withdrawals_query = db.session.query(SavingsUpdate)\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'withdrawal')
        
        # Apply time period filter if needed
        if start_date:
            deposits_query = deposits_query.filter(SavingsUpdate.created_at >= start_date)
            withdrawals_query = withdrawals_query.filter(SavingsUpdate.created_at >= start_date)
        
        # Get total deposits and withdrawals
        total_deposits = db.session.query(func.sum(SavingsUpdate.amount))\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'deposit')
        
        total_withdrawals = db.session.query(func.sum(SavingsUpdate.amount))\
            .filter(SavingsUpdate.user_id == user_id, SavingsUpdate.type == 'withdrawal')
        
        if start_date:
            total_deposits = total_deposits.filter(SavingsUpdate.created_at >= start_date)
            total_withdrawals = total_withdrawals.filter(SavingsUpdate.created_at >= start_date)
        
        total_deposits = total_deposits.scalar() or 0
        total_withdrawals = total_withdrawals.scalar() or 0
        
        # Get largest deposit and withdrawal
        largest_deposit = deposits_query.order_by(desc(SavingsUpdate.amount)).first()
        largest_withdrawal = withdrawals_query.order_by(desc(SavingsUpdate.amount)).first()
        
        # Get deposit and withdrawal counts
        deposit_count = deposits_query.count()
        withdrawal_count = withdrawals_query.count()
        
        # Calculate averages
        avg_deposit = total_deposits / deposit_count if deposit_count > 0 else 0
        avg_withdrawal = total_withdrawals / withdrawal_count if withdrawal_count > 0 else 0
        
        return {
            'total_deposits': float(total_deposits),
            'total_withdrawals': float(total_withdrawals),
            'net_savings': float(total_deposits - total_withdrawals),
            'deposit_count': deposit_count,
            'withdrawal_count': withdrawal_count,
            'avg_deposit': float(avg_deposit),
            'avg_withdrawal': float(avg_withdrawal),
            'largest_deposit': largest_deposit.to_dict() if largest_deposit else None,
            'largest_withdrawal': largest_withdrawal.to_dict() if largest_withdrawal else None,
            'period': period
        }