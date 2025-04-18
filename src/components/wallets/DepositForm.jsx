// frontend/src/components/wallets/DepositForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const DepositForm = ({ walletId, onSuccess }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      console.log(`Deposited ${amount} to wallet ${walletId}`);
      setIsSubmitting(false);
      onSuccess();
    }, 1000);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="Amount (KES)"
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        min="1"
        step="0.01"
        required
      />
      
      <Input
        label="Description (Optional)"
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="e.g. Salary deposit, Gift money"
      />
      
      <Button 
        type="submit" 
        className="w-full mt-4"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Processing...' : 'Deposit'}
      </Button>
    </form>
  );
};

export default DepositForm;