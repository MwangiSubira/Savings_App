// frontend/src/components/goals/GoalList.jsx
import React, { useState } from 'react';
import GoalCard from './GoalCard';
import Button from '../common/Button';
import Modal from '../common/Modal';
import GoalForm from './GoalForm';

const GoalList = ({ goals, onGoalCreated }) => {
  const [showCreateModal, setShowCreateModal] = useState(false);

  const handleCreateGoal = (goalData) => {
    // In a real app, this would call an API
    onGoalCreated({
      ...goalData,
      id: Date.now(),
      currentAmount: 0,
      createdAt: new Date().toISOString(),
    });
    setShowCreateModal(false);
  };

  return (
    <div className="pb-16"> {/* Padding for bottom navbar */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">My Goals</h2>
        <Button onClick={() => setShowCreateModal(true)}>
          + New Goal
        </Button>
      </div>

      {goals.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <p className="text-gray-600 mb-4">You don't have any goals yet</p>
          <Button onClick={() => setShowCreateModal(true)}>
            Create Your First Goal
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          {goals.map((goal) => (
            <GoalCard key={goal.id} goal={goal} />
          ))}
        </div>
      )}

      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Goal"
      >
        <GoalForm onSubmit={handleCreateGoal} />
      </Modal>
    </div>
  );
};

export default GoalList;