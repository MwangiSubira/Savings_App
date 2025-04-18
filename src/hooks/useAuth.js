// frontend/src/hooks/useAuth.js
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const useAuthRedirect = (requireAuth = true, redirectPath = '/login') => {
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading) {
      if (requireAuth && !isAuthenticated) {
        navigate(redirectPath);
      } else if (!requireAuth && isAuthenticated) {
        navigate('/dashboard');
      }
    }
  }, [isAuthenticated, isLoading, navigate, requireAuth, redirectPath]);

  return { isAuthenticated, isLoading };
};

export default useAuthRedirect;