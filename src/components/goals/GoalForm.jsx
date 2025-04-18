// frontend/src/components/goals/GoalForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const GoalForm = ({ onSubmit, initialData = {}, buttonText = 'Create Goal' }) => {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
    targetAmount: initialData.targetAmount || '',
    targetDate: initialData.targetDate || '',
    description: initialData.description || '',
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
      targetAmount: parseFloat(formData.targetAmount),
      targetDate: formData.targetDate,
      description: formData.description,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="Goal Name"
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="e.g. New Car, Vacation, Emergency Fund"
        required
      />
      
      <Input
        label="Target Amount (KES)"
        type="number"
        name="targetAmount"
        value={formData.targetAmount}
        onChange={handleChange}
        min="1"
        step="0.01"
        required
      />
      
      <Input
        label="Target Date"
        type="date"
        name="targetDate"
        value={formData.targetDate}
        onChange={handleChange}
        required
      />
      
      <Input
        label="Description (Optional)"
        type="text"
        name="description"
        value={formData.description}
        onChange={handleChange}
        placeholder="Brief description of your goal"
      />
      
      <Button type="submit" className="w-full mt-4">
        {buttonText}
      </Button>
    </form>
  );
};

export default GoalForm;