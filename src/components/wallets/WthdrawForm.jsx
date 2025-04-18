// frontend/src/components/wallets/WithdrawForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const WithdrawForm = ({ walletId, currentBalance, onSuccess }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (parseFloat(amount) > currentBalance) {
      setError('Amount exceeds available balance');
      return;
    }

    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      console.log(`Withdrew ${amount} from wallet ${walletId}`);
      setIsSubmitting(false);
      onSuccess();
    }, 1000);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-4 p-3 bg-blue-50 rounded-lg">
        <p className="text-sm text-gray-600">Available Balance</p>
        <p className="font-bold text-lg">KES {currentBalance.toLocaleString()}</p>
      </div>
      
      <Input
        label="Amount (KES)"
        type="number"
        value={amount}
        onChange={(e) => {
          setAmount(e.target.value);
          setError('');
        }}
        min="1"
        max={currentBalance}
        step="0.01"
        required
      />
      
      {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
      
      <Input
        label="Description (Optional)"
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="e.g. Rent payment, Groceries"
      />
      
      <Button 
        type="submit" 
        className="w-full mt-4"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Processing...' : 'Withdraw'}
      </Button>
    </form>
  );
};

export default WithdrawForm;