// frontend/src/components/goals/GoalProgress.jsx
import React from 'react';

const GoalProgress = ({ goal }) => {
  // Calculate various progress metrics
  const progressPercentage = Math.min(
    Math.round((goal.currentAmount / goal.targetAmount) * 100),
    100
  );
  const remainingAmount = goal.targetAmount - goal.currentAmount;
  const today = new Date();
  const targetDate = new Date(goal.targetDate);
  const daysRemaining = Math.max(
    Math.ceil((targetDate - today) / (1000 * 60 * 60 * 24)),
    0
  );
  const dailyAmountNeeded = daysRemaining > 0 ? remainingAmount / daysRemaining : remainingAmount;

  return (
    <div className="bg-white rounded-xl shadow-md p-4">
      <h3 className="font-bold text-lg mb-4">Goal Progress</h3>
      
      <div className="space-y-4">
        <div>
          <div className="flex justify-between mb-1">
            <span className="text-sm font-medium">Progress</span>
            <span className="text-sm font-medium">{progressPercentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">Current Amount</p>
            <p className="font-bold">KES {goal.currentAmount.toLocaleString()}</p>
          </div>
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">Target Amount</p>
            <p className="font-bold">KES {goal.targetAmount.toLocaleString()}</p>
          </div>
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">Remaining</p>
            <p className="font-bold">KES {remainingAmount.toLocaleString()}</p>
          </div>
          <div className="bg-blue-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">Days Left</p>
            <p className="font-bold">{daysRemaining}</p>
          </div>
        </div>

        {daysRemaining > 0 && (
          <div className="bg-green-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">Daily Amount Needed</p>
            <p className="font-bold">KES {dailyAmountNeeded.toFixed(2).toLocaleString()}</p>
          </div>
        )}

        {goal.description && (
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-sm text-gray-600">Description</p>
            <p className="font-medium">{goal.description}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default GoalProgress;