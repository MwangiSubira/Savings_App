// frontend/src/components/auth/LoginForm.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../common/Input';
import Button from '../common/Button';

const LoginForm = () => {
  const [step, setStep] = useState(1);
  const [phone, setPhone] = useState('');
  const [pin, setPin] = useState(['', '', '', '']);
  const navigate = useNavigate();

  const handlePhoneSubmit = (e) => {
    e.preventDefault();
    setStep(2);
  };

  const handlePinSubmit = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  const handlePinChange = (index, value) => {
    const newPin = [...pin];
    newPin[index] = value;
    setPin(newPin);
  };

  return (
    <div className="max-w-md mx-auto w-full">
      {step === 1 ? (
        <form onSubmit={handlePhoneSubmit}>
          <h1 className="text-2xl font-bold text-center mb-6">Log into your SACCO account</h1>
          <p className="text-center mb-6">Welcome back, we missed you!</p>
          
          <Input
            label="Enter your phone number"
            type="tel"
            prefix="+254"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
          
          <Button type="submit" className="w-full mt-4">
            Next
          </Button>
          
          <div className="mt-6 text-center text-sm">
            <p className="text-gray-600">
              Not a SACCO member? <a href="/register" className="text-blue-600">Join one now</a>
            </p>
            <p className="text-gray-600 mt-1">
              Need Help? <a href="/help" className="text-blue-600">Click here</a>
            </p>
          </div>
        </form>
      ) : (
        <form onSubmit={handlePinSubmit}>
          <h1 className="text-xl font-bold text-center mb-2">Your account is secure</h1>
          <p className="text-center mb-6">Enter your 4 digit PIN</p>
          
          <div className="flex justify-center gap-2 mb-6">
            {[0, 1, 2, 3].map((index) => (
              <input
                key={index}
                type="password"
                maxLength={1}
                value={pin[index]}
                onChange={(e) => handlePinChange(index, e.target.value)}
                className="w-12 h-12 border border-gray-300 rounded-lg text-center text-xl focus:ring-blue-500 focus:border-blue-500"
                required
              />
            ))}
          </div>
          
          <Button type="submit" className="w-full">
            Log in
          </Button>
          
          <div className="mt-4 text-center">
            <a href="/reset-pin" className="text-blue-600 text-sm">
              Reset your PIN
            </a>
          </div>
          
          <div className="mt-6 text-center text-xs text-gray-500">
            <a href="/security" className="underline">
              Security Policy
            </a>
          </div>
        </form>
      )}
    </div>
  );
};

export default LoginForm;