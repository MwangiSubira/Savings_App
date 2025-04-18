// frontend/src/services/authService.js
import api from './api';

const authService = {
  async login(credentials) {
    const response = await api.post('/auth/login', credentials);
    localStorage.setItem('token', response.data.token);
    return response.data.user;
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData);
    localStorage.setItem('token', response.data.token);
    return response.data.user;
  },

  async logout() {
    localStorage.removeItem('token');
    await api.post('/auth/logout');
  },

  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      return null;
    }
  },

  async forgotPassword(email) {
    await api.post('/auth/forgot-password', { email });
  },

  async resetPassword(token, newPassword) {
    await api.post('/auth/reset-password', { token, newPassword });
  },
};

export default authService;