// frontend/src/pages/Auth/Register.jsx
import React from 'react';
import RegisterForm from '../../components/auth/RegisterForm';
import useAuthRedirect from '../../hooks/useAuth';

const Register = () => {
  useAuthRedirect(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <RegisterForm />
      </div>
    </div>
  );
};

export default Register;