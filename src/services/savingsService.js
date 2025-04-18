// frontend/src/services/savingsService.js
import api from './api';

const savingsService = {
  async getSavingsUpdates(params = {}) {
    const response = await api.get('/savings', { params });
    return response.data;
  },

  async createSavingsUpdate(data) {
    const response = await api.post('/savings', data);
    return response.data;
  },

  async getSavingsSummary() {
    const response = await api.get('/savings/summary');
    return response.data;
  },

  async getMonthlyBreakdown() {
    const response = await api.get('/savings/monthly');
    return response.data;
  },
};

export default savingsService;