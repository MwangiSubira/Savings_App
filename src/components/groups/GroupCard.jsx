// frontend/src/components/groups/GroupCard.jsx
import React, { useState } from 'react';
import Button from '../common/Button';
import Modal from '../common/Modal';
import MemberList from './MemberList';

const GroupCard = ({ group }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [showMembersModal, setShowMembersModal] = useState(false);

  return (
    <div className="bg-white rounded-xl shadow-md p-4 mb-4">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-bold text-lg">{group.name}</h3>
          <p className="text-gray-600 text-sm">
            {group.memberCount} member{group.memberCount !== 1 ? 's' : ''}
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

      {showDetails && (
        <div className="mt-4">
          {group.description && (
            <p className="text-gray-700 mb-3">{group.description}</p>
          )}

          <div className="flex justify-between py-2 border-b">
            <span>Created By</span>
            <span className="font-medium">{group.createdBy}</span>
          </div>
          <div className="flex justify-between py-2">
            <span>Created On</span>
            <span className="font-medium">
              {new Date(group.createdAt).toLocaleDateString()}
            </span>
          </div>

          <div className="flex gap-2 mt-4">
            <Button 
              className="flex-1"
              onClick={() => setShowMembersModal(true)}
            >
              View Members
            </Button>
            {group.isAdmin && (
              <Button 
                variant="secondary" 
                className="flex-1"
                onClick={() => console.log('Manage group')}
              >
                Manage
              </Button>
            )}
          </div>
        </div>
      )}

      <Modal 
        isOpen={showMembersModal} 
        onClose={() => setShowMembersModal(false)}
        title={`Members of ${group.name}`}
        size="lg"
      >
        <MemberList 
          members={group.members} 
          isAdmin={group.isAdmin}
          onMemberRemoved={() => setShowMembersModal(false)}
        />
      </Modal>
    </div>
  );
};

export default GroupCard;