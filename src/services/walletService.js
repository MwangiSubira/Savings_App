// frontend/src/services/walletService.js
import api from './api';

const walletService = {
  async getWallets() {
    const response = await api.get('/wallets');
    return response.data;
  },

  async createWallet(walletData) {
    const response = await api.post('/wallets', walletData);
    return response.data;
  },

  async updateWallet(walletId, walletData) {
    const response = await api.put(`/wallets/${walletId}`, walletData);
    return response.data;
  },

  async deleteWallet(walletId) {
    await api.delete(`/wallets/${walletId}`);
  },

  async deposit(walletId, amount, description) {
    const response = await api.post(`/wallets/${walletId}/deposit`, {
      amount,
      description,
    });
    return response.data;
  },

  async withdraw(walletId, amount, description) {
    const response = await api.post(`/wallets/${walletId}/withdraw`, {
      amount,
      description,
    });
    return response.data;
  },

  async getWalletHistory(walletId) {
    const response = await api.get(`/wallets/${walletId}/history`);
    return response.data;
  },
};

export default walletService;