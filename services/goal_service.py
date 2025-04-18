from app import db
from app.models.goal import Goal
from app.models.savings import SavingsUpdate
from app.models.wallet import Wallet
from decimal import Decimal

class GoalService:
    def get_user_goals(self, user_id):
        """Get all goals for a user"""
        return Goal.query.filter_by(user_id=user_id).all()
    
    def get_goal(self, goal_id, user_id):
        """Get a specific goal"""
        return Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    def create_goal(self, user_id, target_amount, time_period, description=None, name=None):
        """Create a new savings goal"""
        if not isinstance(target_amount, (int, float, Decimal)) or target_amount <= 0:
            raise ValueError("Target amount must be a positive number")
        
        goal = Goal(
            user_id=user_id,
            target_amount=target_amount,
            time_period=time_period,
            description=description,
            name=name
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return goal
    
    def update_goal(self, goal_id, user_id, target_amount=None, time_period=None, description=None, name=None):
        """Update a goal's details"""
        goal = self.get_goal(goal_id, user_id)
        
        if not goal:
            return None
        
        if target_amount is not None:
            if not isinstance(target_amount, (int, float, Decimal)) or target_amount <= 0:
                raise ValueError("Target amount must be a positive number")
            goal.target_amount = target_amount
        
        if time_period is not None:
            goal.time_period = time_period
        
        if description is not None:
            goal.description = description
        
        if name is not None:
            goal.name = name
        
        db.session.commit()
        return goal
    
    def delete_goal(self, goal_id, user_id):
        """Delete a goal"""
        goal = self.get_goal(goal_id, user_id)
        
        if not goal:
            return False
        
        db.session.delete(goal)
        db.session.commit()
        
        return True
    
    def add_progress(self, goal_id, user_id, amount, wallet_id, description=None):
        """Add progress to a goal by transferring from a wallet"""
        # Verify goal exists and belongs to user
        goal = self.get_goal(goal_id, user_id)
        if not goal:
            raise ValueError("Goal not found or unauthorized")
        
        # Verify wallet exists and belongs to user
        wallet = Wallet.query.filter_by(id=wallet_id, user_id=user_id).first()
        if not wallet:
            raise ValueError("Wallet not found or unauthorized")
        
        # Validate amount
        if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        
        # Ensure sufficient funds in wallet
        if wallet.amount < Decimal(str(amount)):
            raise ValueError("Insufficient funds in wallet")
        
        # Update wallet balance
        wallet.withdraw(amount)
        
        # Update goal's current amount
        goal.add_progress(amount)
        
        # Create savings update record
        savings_update = SavingsUpdate(
            user_id=user_id,
            wallet_id=wallet_id,
            goal_id=goal_id,
            amount=amount,
            type='goal_contribution',
            description=description or f"Contribution to goal: {goal.name}"
        )
        
        db.session.add(savings_update)
        db.session.commit()
        
        return goal, wallet, savings_update
    
    def get_goal_history(self, goal_id, user_id):
        """Get contribution history for a goal"""
        # First verify goal ownership
        goal = self.get_goal(goal_id, user_id)
        
        if not goal:
            raise ValueError("Goal not found or unauthorized")
        
        # Get all savings updates for this goal
        history = SavingsUpdate.query.filter_by(
            goal_id=goal_id
        ).order_by(SavingsUpdate.updated_at.desc()).all()
        
        return history
    
    def calculate_goal_progress(self, goal_id, user_id):
        """Calculate the progress percentage and remaining amount for a goal"""
        goal = self.get_goal(goal_id, user_id)
        
        if not goal:
            raise ValueError("Goal not found or unauthorized")
        
        progress_percentage = (goal.current_amount / goal.target_amount) * 100
        remaining_amount = goal.target_amount - goal.current_amount
        
        return {
            "goal": goal.to_dict(),
            "progress_percentage": float(progress_percentage),
            "remaining_amount": float(remaining_amount)
        }
    
    def calculate_daily_savings_needed(self, goal_id, user_id):
        """Calculate how much needs to be saved daily to reach the goal on time"""
        goal = self.get_goal(goal_id, user_id)
        
        if not goal:
            raise ValueError("Goal not found or unauthorized")
        
        remaining_amount = goal.target_amount - goal.current_amount
        
        # Get remaining days based on time period and creation date
        import datetime
        from datetime import date
        today = date.today()
        
        # Calculate end date from creation date and time period
        end_date = goal.created_at.date() + goal.time_period
        
        # If the end date is in the past, return a special message
        if end_date < today:
            return {
                "goal": goal.to_dict(),
                "daily_amount": None,
                "is_overdue": True,
                "days_remaining": 0
            }
        
        # Calculate days remaining
        days_remaining = (end_date - today).days
        
        # If no days remaining but not overdue, it's due today
        if days_remaining == 0:
            days_remaining = 1
        
        # Calculate daily amount needed
        daily_amount = remaining_amount / days_remaining if days_remaining > 0 else remaining_amount
        
        return {
            "goal": goal.to_dict(),
            "daily_amount": float(daily_amount),
            "is_overdue": False,
            "days_remaining": days_remaining
        }