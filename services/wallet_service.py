from app import db
from app.models.wallet import Wallet
from app.models.savings import SavingsUpdate
from decimal import Decimal

class WalletService:
    def get_user_wallets(self, user_id):
        """Get all wallets for a user"""
        return Wallet.query.filter_by(user_id=user_id).all()
    
    def get_wallet(self, wallet_id, user_id):
        """Get a specific wallet"""
        return Wallet.query.filter_by(id=wallet_id, user_id=user_id).first()
    
    def create_wallet(self, user_id, name=None, initial_amount=0):
        """Create a new wallet"""
        if initial_amount < 0:
            raise ValueError("Initial amount cannot be negative")
        
        wallet = Wallet(
            user_id=user_id,
            name=name,
            amount=initial_amount
        )
        
        db.session.add(wallet)
        db.session.commit()
        
        # If there's an initial amount, create a savings update record
        if initial_amount > 0:
            savings_update = SavingsUpdate(
                user_id=user_id,
                wallet_id=wallet.id,
                amount=initial_amount,
                type='deposit',
                description="Initial deposit"
            )
            
            db.session.add(savings_update)
            db.session.commit()
        
        return wallet
    
    def update_wallet(self, wallet_id, user_id, name=None):
        """Update a wallet's details"""
        wallet = self.get_wallet(wallet_id, user_id)
        
        if not wallet:
            return None
        
        if name is not None:
            wallet.name = name
        
        db.session.commit()
        return wallet
    
    def delete_wallet(self, wallet_id, user_id):
        """Delete a wallet"""
        wallet = self.get_wallet(wallet_id, user_id)
        
        if not wallet:
            return False
        
        db.session.delete(wallet)
        db.session.commit()
        
        return True
    
    def deposit(self, wallet_id, user_id, amount, goal_id=None, description=None):
        """Add funds to a wallet"""
        wallet = self.get_wallet(wallet_id, user_id)
        
        if not wallet:
            raise ValueError("Wallet not found")
        
        if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        
        # Update wallet balance
        wallet.deposit(amount)
        
        # Create savings update record
        savings_update = SavingsUpdate(
            user_id=user_id,
            wallet_id=wallet_id,
            goal_id=goal_id,
            amount=amount,
            type='deposit',
            description=description
        )
        
        db.session.add(savings_update)
        db.session.commit()
        
        return wallet, savings_update
    
    def withdraw(self, wallet_id, user_id, amount, description=None):
        """Withdraw funds from a wallet"""
        wallet = self.get_wallet(wallet_id, user_id)
        
        if not wallet:
            raise ValueError("Wallet not found")
        
        if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        
        # Ensure sufficient funds
        if Decimal(str(amount)) > wallet.amount:
            raise ValueError("Insufficient funds")
        
        # Update wallet balance
        wallet.withdraw(amount)
        
        # Create savings update record
        savings_update = SavingsUpdate(
            user_id=user_id,
            wallet_id=wallet_id,
            amount=amount,
            type='withdrawal',
            description=description
        )
        
        db.session.add(savings_update)
        db.session.commit()
        
        return wallet, savings_update
    
    def get_wallet_history(self, wallet_id, user_id):
        """Get transaction history for a wallet"""
        # First verify wallet ownership
        wallet = self.get_wallet(wallet_id, user_id)
        
        if not wallet:
            raise ValueError("Wallet not found or unauthorized")
        
        # Get all savings updates for this wallet
        history = SavingsUpdate.query.filter_by(
            wallet_id=wallet_id
        ).order_by(SavingsUpdate.updated_at.desc()).all()
        
        return history