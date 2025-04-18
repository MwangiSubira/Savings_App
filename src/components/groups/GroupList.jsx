// frontend/src/components/groups/GroupList.jsx
import React, { useState } from 'react';
import GroupCard from './GroupCard';
import Button from '../common/Button';
import Modal from '../common/Modal';
import GroupForm from './GroupForm';

const GroupList = ({ groups, onGroupCreated }) => {
  const [showCreateModal, setShowCreateModal] = useState(false);

  const handleCreateGroup = (groupData) => {
    // In a real app, this would call an API
    onGroupCreated({
      ...groupData,
      id: Date.now(),
      memberCount: 1,
      createdAt: new Date().toISOString(),
      createdBy: "You",
      isAdmin: true,
      members: [{ id: 1, name: "You", isAdmin: true, joinedAt: new Date().toISOString() }]
    });
    setShowCreateModal(false);
  };

  return (
    <div className="pb-16"> {/* Padding for bottom navbar */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">My Groups</h2>
        <Button onClick={() => setShowCreateModal(true)}>
          + New Group
        </Button>
      </div>

      {groups.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <p className="text-gray-600 mb-4">You're not in any groups yet</p>
          <Button onClick={() => setShowCreateModal(true)}>
            Create New Group
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          {groups.map((group) => (
            <GroupCard key={group.id} group={group} />
          ))}
        </div>
      )}

      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Group"
      >
        <GroupForm onSubmit={handleCreateGroup} />
      </Modal>
    </div>
  );
};

export default GroupList;