// frontend/src/components/groups/MemberList.jsx
import React from 'react';
import MemberManagement from './MemberManagement';

const MemberList = ({ members, isAdmin, onMemberRemoved }) => {
  const handleRemoveMember = (memberId) => {
    if (window.confirm('Are you sure you want to remove this member?')) {
      console.log(`Removing member ${memberId}`);
      onMemberRemoved();
    }
  };

  return (
    <div>
      <div className="divide-y">
        {members.map((member) => (
          <div key={member.id} className="py-3 flex justify-between items-center">
            <div>
              <p className="font-medium">
                {member.name || member.email}
                {member.isAdmin && (
                  <span className="ml-2 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded">
                    Admin
                  </span>
                )}
              </p>
              <p className="text-sm text-gray-500">
                Joined {new Date(member.joinedAt).toLocaleDateString()}
              </p>
            </div>
            {isAdmin && !member.isAdmin && (
              <button
                onClick={() => handleRemoveMember(member.id)}
                className="text-red-500 hover:text-red-700 text-sm"
              >
                Remove
              </button>
            )}
          </div>
        ))}
      </div>

      {isAdmin && (
        <MemberManagement 
          groupId={members[0]?.groupId} 
          onMemberAdded={(newMember) => console.log('Add member:', newMember)}
        />
      )}
    </div>
  );
};

export default MemberList;