// frontend/src/components/goals/ProgressForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const ProgressForm = ({ goalId, remainingAmount, onSuccess }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const amountNum = parseFloat(amount);
    if (amountNum > remainingAmount) {
      setError(`Amount exceeds remaining goal amount (KES ${remainingAmount.toLocaleString()})`);
      return;
    }

    if (amountNum <= 0) {
      setError('Amount must be greater than zero');
      return;
    }

    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      console.log(`Added ${amount} to goal ${goalId}`);
      setIsSubmitting(false);
      onSuccess();
    }, 1000);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-4 p-3 bg-blue-50 rounded-lg">
        <p className="text-sm text-gray-600">Remaining to Reach Goal</p>
        <p className="font-bold text-lg">KES {remainingAmount.toLocaleString()}</p>
      </div>
      
      <Input
        label="Amount to Add (KES)"
        type="number"
        value={amount}
        onChange={(e) => {
          setAmount(e.target.value);
          setError('');
        }}
        min="1"
        max={remainingAmount}
        step="0.01"
        required
      />
      
      {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
      
      <Input
        label="Description (Optional)"
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="e.g. Monthly savings, Bonus"
      />
      
      <Button 
        type="submit" 
        className="w-full mt-4"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Processing...' : 'Add to Goal'}
      </Button>
    </form>
  );
};

export default ProgressForm;