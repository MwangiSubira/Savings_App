// frontend/src/components/common/Navbar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  const navItems = [
    { path: '/loans', icon: '🏦', label: 'Loans' },
    { path: '/savings', icon: '💰', label: 'Savings' },
    { path: '/history', icon: '📊', label: 'History' },
    { path: '/profile', icon: '👤', label: 'Profile' },
    { path: '/help', icon: '❓', label: 'Help' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white shadow-lg flex justify-around py-3 px-2">
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            `flex flex-col items-center ${isActive ? 'text-blue-600' : 'text-gray-500'}`
          }
        >
          <span className="text-xl">{item.icon}</span>
          <span className="text-xs mt-1">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
};

export default Navbar;