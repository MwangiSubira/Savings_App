// frontend/src/components/common/Input.jsx
import React from 'react';

const Input = ({ label, type = 'text', prefix, className = '', ...props }) => {
  return (
    <div className={`mb-4 ${className}`}>
      {label && <label className="block text-sm font-medium mb-1">{label}</label>}
      {prefix ? (
        <div className="flex">
          <div className="bg-gray-100 px-4 py-2 rounded-l-lg border border-r-0 border-gray-300">
            {prefix}
          </div>
          <input
            type={type}
            className="flex-1 border border-gray-300 rounded-r-lg px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
            {...props}
          />
        </div>
      ) : (
        <input
          type={type}
          className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-blue-500 focus:border-blue-500"
          {...props}
        />
      )}
    </div>
  );
};

export default Input;