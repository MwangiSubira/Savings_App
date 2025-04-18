// frontend/src/pages/Auth/Login.jsx
import React from 'react';
import LoginForm from '../../components/auth/LoginForm';
import useAuthRedirect from '../../hooks/useAuth';

const Login = () => {
  useAuthRedirect(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <LoginForm />
      </div>
    </div>
  );
};

export default Login;