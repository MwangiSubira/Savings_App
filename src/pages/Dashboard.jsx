// frontend/src/pages/Dashboard.jsx
import React from 'react';
import DashboardOverview from '../../components/dashboard/DashboardOverview';
import useAuthRedirect from '../../hooks/useAuth';

const Dashboard = () => {
  const { user } = useAuthRedirect();

  // Sample data - in a real app, this would come from API
  const wallets = [
    { id: 1, name: 'Main Wallet', balance: 25000, lastDeposit: 5000, lastWithdrawal: 2000 },
  ];
  const goals = [
    { id: 1, name: 'New Car', targetAmount: 500000, currentAmount: 125000, targetDate: '2023-12-31' },
  ];
  const groups = [
    { id: 1, name: 'Family Group', memberCount: 5 },
  ];

  return (
    <DashboardOverview 
      user={user} 
      wallets={wallets} 
      goals={goals} 
      groups={groups} 
    />
  );
};

export default Dashboard;