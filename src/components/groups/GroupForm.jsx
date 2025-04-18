// frontend/src/components/groups/GroupForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const GroupForm = ({ onSubmit, initialData = {}, buttonText = 'Create Group' }) => {
  const [formData, setFormData] = useState({
    name: initialData.name || '',
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
      description: formData.description,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="Group Name"
        type="text"
        name="name"
        value={formData.name}
        onChange={handleChange}
        placeholder="e.g. Family Savings, Investment Group"
        required
      />
      
      <Input
        label="Description (Optional)"
        type="text"
        name="description"
        value={formData.description}
        onChange={handleChange}
        placeholder="What's this group about?"
        as="textarea"
        rows={3}
      />
      
      <Button type="submit" className="w-full mt-4">
        {buttonText}
      </Button>
    </form>
  );
};

export default GroupForm;