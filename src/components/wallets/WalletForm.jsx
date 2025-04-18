// frontend/src/components/wallets/WalletForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const WalletForm = ({ onSubmit, initialData = {}, buttonText = 'Create Wallet' }) => {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
    initialBalance: initialData.balance || 0,
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name: formData.name,
      balance: parseFloat(formData.initialBalance) || 0,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="Wallet Name"
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="e.g. Main Savings, Emergency Fund"
      />
      
      <Input
        label="Initial Balance (KES)"
        type="number"
        name="initialBalance"
        value={formData.initialBalance}
        onChange={handleChange}
        min="0"
        step="0.01"
      />
      
      <Button type="submit" className="w-full mt-4">
        {buttonText}
      </Button>
    </form>
  );
};

export default WalletForm;