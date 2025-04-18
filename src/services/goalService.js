// frontend/src/services/goalService.js
import api from './api';

const goalService = {
  async getGoals() {
    const response = await api.get('/goals');
    return response.data;
  },

  async createGoal(goalData) {
    const response = await api.post('/goals', goalData);
    return response.data;
  },

  async updateGoal(goalId, goalData) {
    const response = await api.put(`/goals/${goalId}`, goalData);
    return response.data;
  },

  async deleteGoal(goalId) {
    await api.delete(`/goals/${goalId}`);
  },

  async addProgress(goalId, walletId, amount, description) {
    const response = await api.post(`/goals/${goalId}/progress`, {
      walletId,
      amount,
      description,
    });
    return response.data;
  },

  async getGoalHistory(goalId) {
    const response = await api.get(`/goals/${goalId}/history`);
    return response.data;
  },
};

export default goalService;