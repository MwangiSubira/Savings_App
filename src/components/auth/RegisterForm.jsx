// frontend/src/components/auth/RegisterForm.jsx
import React, { useState } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle registration logic
  };

  return (
    <div className="max-w-md mx-auto w-full">
      <h1 className="text-2xl font-bold text-center mb-6">Join KCS Sacco</h1>
      
      <form onSubmit={handleSubmit}>
        <Input
          label="Full Name"
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        
        <Input
          label="Phone Number"
          type="tel"
          name="phone"
          prefix="+254"
          value={formData.phone}
          onChange={handleChange}
          required
        />
        
        <Input
          label="Email Address"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        
        <Input
          label="Password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        
        <Input
          label="Confirm Password"
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        
        <Button type="submit" className="w-full mt-4">
          Register
        </Button>
      </form>
      
      <div className="mt-4 text-center text-sm">
        <p className="text-gray-600">
          Already have an account? <a href="/login" className="text-blue-600">Log in</a>
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;