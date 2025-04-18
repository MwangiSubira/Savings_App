// frontend/src/components/dashboard/SummaryStats.jsx
import React from 'react';

const SummaryStats = ({ 
  totalBalance, 
  walletCount, 
  goalCount, 
  groupCount,
  goalsProgress
}) => {
  return (
    <div className="grid grid-cols-2 gap-3">
      <div className="bg-white rounded-lg shadow p-3">
        <p className="text-sm text-gray-600">Total Balance</p>
        <p className="text-xl font-bold">KES {totalBalance.toLocaleString()}</p>
      </div>
      <div className="bg-white rounded-lg shadow p-3">
        <p className="text-sm text-gray-600">Wallets</p>
        <p className="text-xl font-bold">{walletCount}</p>
      </div>
      <div className="bg-white rounded-lg shadow p-3">
        <p className="text-sm text-gray-600">Goals Progress</p>
        <p className="text-xl font-bold">{Math.round(goalsProgress * 100)}%</p>
      </div>
      <div className="bg-white rounded-lg shadow p-3">
        <p className="text-sm text-gray-600">Groups</p>
        <p className="text-xl font-bold">{groupCount}</p>
      </div>
    </div>
  );
};

export default SummaryStats;