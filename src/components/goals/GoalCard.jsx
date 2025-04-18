// frontend/src/components/goals/GoalCard.jsx
import React, { useState } from 'react';
import Button from '../common/Button';
import Modal from '../common/Modal';
import ProgressForm from './ProgressForm';

const GoalCard = ({ goal }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [showProgressModal, setShowProgressModal] = useState(false);
  
  // Calculate progress percentage
  const progressPercentage = Math.min(
    Math.round((goal.currentAmount / goal.targetAmount) * 100),
    100
  );

  return (
    <div className="bg-white rounded-xl shadow-md p-4 mb-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-bold text-lg">{goal.name}</h3>
          <p className="text-gray-600 text-sm">
            Target: KES {goal.targetAmount.toLocaleString()}
          </p>
        </div>
        <Button 
          size="small" 
          variant="outline" 
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Hide' : 'Show'}
        </Button>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-200 rounded-full h-2.5 mt-3">
        <div 
          className="bg-blue-600 h-2.5 rounded-full" 
          style={{ width: `${progressPercentage}%` }}
        ></div>
      </div>
      <p className="text-right text-sm text-gray-600 mt-1">
        {progressPercentage}% complete
      </p>

      {showDetails && (
        <div className="mt-4">
          <div className="flex justify-between py-2 border-b">
            <span>Current Amount</span>
            <span className="font-medium">KES {goal.currentAmount.toLocaleString()}</span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span>Remaining</span>
            <span className="font-medium">
              KES {(goal.targetAmount - goal.currentAmount).toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between py-2">
            <span>Target Date</span>
            <span className="font-medium">
              {new Date(goal.targetDate).toLocaleDateString()}
            </span>
          </div>

          <Button 
            className="w-full mt-4"
            onClick={() => setShowProgressModal(true)}
          >
            Add Progress
          </Button>
        </div>
      )}

      <Modal 
        isOpen={showProgressModal} 
        onClose={() => setShowProgressModal(false)}
        title="Add Progress to Goal"
      >
        <ProgressForm 
          goalId={goal.id} 
          remainingAmount={goal.targetAmount - goal.currentAmount}
          onSuccess={() => {
            setShowProgressModal(false);
            setShowDetails(true);
          }} 
        />
      </Modal>
    </div>
  );
};

export default GoalCard;