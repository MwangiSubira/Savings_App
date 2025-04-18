// frontend/src/components/groups/MemberManagement.jsx
import React, { useState } from 'react';
import Button from '../common/Button';
import Modal from '../common/Modal';
import Input from '../common/Input';

const MemberManagement = ({ groupId, onMemberAdded }) => {
  const [email, setEmail] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddMember = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      onMemberAdded({
        id: Date.now(),
        email,
        isAdmin,
        joinedAt: new Date().toISOString()
      });
      setEmail('');
      setIsAdmin(false);
      setIsSubmitting(false);
    }, 1000);
  };

  return (
    <div className="mt-6">
      <h4 className="font-bold mb-2">Add New Member</h4>
      <form onSubmit={handleAddMember}>
        <div className="flex gap-2">
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Member's email"
            className="flex-1"
            required
          />
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Adding...' : 'Add'}
          </Button>
        </div>
        <label className="flex items-center mt-2">
          <input
            type="checkbox"
            checked={isAdmin}
            onChange={(e) => setIsAdmin(e.target.checked)}
            className="mr-2"
          />
          <span className="text-sm">Make group admin</span>
        </label>
      </form>
    </div>
  );
};

export default MemberManagement;