// frontend/src/pages/Groups.jsx
import React, { useState, useEffect } from 'react';
import GroupList from '../../components/groups/GroupList';
import useAuthRedirect from '../../hooks/useAuth';

const Groups = () => {
  useAuthRedirect();
  const [groups, setGroups] = useState([]);

  // In a real app, you would fetch groups from API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setGroups([
        { 
          id: 1, 
          name: 'Family Group', 
          memberCount: 5,
          description: 'Our family savings group',
          createdAt: '2023-01-01',
          createdBy: 'You',
          isAdmin: true,
          members: [
            { id: 1, name: 'You', isAdmin: true, joinedAt: '2023-01-01' },
            { id: 2, name: 'Jane', isAdmin: false, joinedAt: '2023-01-15' },
          ]
        },
      ]);
    }, 500);
  }, []);

  const handleGroupCreated = (newGroup) => {
    setGroups([...groups, { 
      ...newGroup, 
      id: Date.now(),
      memberCount: 1,
      createdAt: new Date().toISOString(),
      createdBy: "You",
      isAdmin: true,
      members: [{ id: 1, name: "You", isAdmin: true, joinedAt: new Date().toISOString() }]
    }]);
  };

  return (
    <div className="container mx-auto px-4 py-6">
      <GroupList groups={groups} onGroupCreated={handleGroupCreated} />
    </div>
  );
};

export default Groups;