// frontend/src/components/dashboard/DashboardOverview.jsx
import React from 'react';
import SummaryStats from './SummaryStats';
import QuickActions from '../common/QuickActions';
import SavingsChart from './SavingsChart';

const DashboardOverview = ({ user, wallets, goals, groups }) => {
  const totalBalance = wallets.reduce((sum, wallet) => sum + wallet.balance, 0);
  const totalGoalsProgress = goals.reduce(
    (sum, goal) => sum + (goal.currentAmount / goal.targetAmount),
    0
  ) / (goals.length || 1);

  const quickActions = [
    { id: 1, title: 'Add Deposit', icon: '💰', action: '/deposit' },
    { id: 2, title: 'Instant Loan', icon: '🤑', action: '/loans' },
    { id: 3, title: 'Repay Loan', icon: '💳', action: '/repay' },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-blue-600 text-white p-4 rounded-b-3xl">
        <h1 className="text-xl font-bold">KCS Sacco</h1>
        <p className="text-lg">Hi, {user?.name || 'Member'}!</p>
        <p className="text-sm opacity-80">Member ID: {user?.memberId || '5151CWQW'}</p>
      </div>

      <div className="px-4">
        <SummaryStats 
          totalBalance={totalBalance}
          walletCount={wallets.length}
          goalCount={goals.length}
          groupCount={groups.length}
          goalsProgress={totalGoalsProgress}
        />

        <QuickActions actions={quickActions} className="mt-4" />

        <SavingsChart wallets={wallets} className="mt-6" />

        {groups.length > 0 && (
          <div className="mt-6">
            <h2 className="text-lg font-bold mb-2">Your Groups</h2>
            <div className="grid grid-cols-2 gap-3">
              {groups.slice(0, 2).map(group => (
                <div key={group.id} className="bg-white rounded-lg shadow p-3">
                  <h3 className="font-medium">{group.name}</h3>
                  <p className="text-sm text-gray-600">
                    {group.memberCount} member{group.memberCount !== 1 ? 's' : ''}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardOverview;