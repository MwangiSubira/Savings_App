// frontend/src/pages/Profile.jsx
import React from 'react';
import { useAuth } from '../../context/AuthContext';
import useAuthRedirect from '../../hooks/useAuth';

const Profile = () => {
  const { user } = useAuthRedirect();
  const { logout } = useAuth();

  return (
    <div className="container mx-auto px-4 py-6 pb-16">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h1 className="text-2xl font-bold mb-6">Profile</h1>
        
        <div className="space-y-4">
          <div>
            <p className="text-sm text-gray-600">Name</p>
            <p className="font-medium">{user?.name || 'Not available'}</p>
          </div>
          
          <div>
            <p className="text-sm text-gray-600">Email</p>
            <p className="font-medium">{user?.email || 'Not available'}</p>
          </div>
          
          <div>
            <p className="text-sm text-gray-600">Member ID</p>
            <p className="font-medium">{user?.memberId || 'Not available'}</p>
          </div>
          
          <div className="pt-4">
            <button
              onClick={logout}
              className="w-full bg-red-600 text-white py-2 rounded-lg font-bold"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;