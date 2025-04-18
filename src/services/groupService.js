// frontend/src/services/groupService.js
import api from './api';

const groupService = {
  async getGroups() {
    const response = await api.get('/groups');
    return response.data;
  },

  async createGroup(groupData) {
    const response = await api.post('/groups', groupData);
    return response.data;
  },

  async updateGroup(groupId, groupData) {
    const response = await api.put(`/groups/${groupId}`, groupData);
    return response.data;
  },

  async deleteGroup(groupId) {
    await api.delete(`/groups/${groupId}`);
  },

  async addMember(groupId, userId, isAdmin = false) {
    const response = await api.post(`/groups/${groupId}/members`, {
      userId,
      isAdmin,
    });
    return response.data;
  },

  async removeMember(groupId, userId) {
    await api.delete(`/groups/${groupId}/members/${userId}`);
  },

  async getGroupMembers(groupId) {
    const response = await api.get(`/groups/${groupId}/members`);
    return response.data;
  },
};

export default groupService;