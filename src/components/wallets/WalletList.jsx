// frontend/src/components/wallets/WalletList.jsx
import React from 'react';
import WalletCard from './WalletCard';
import Button from '../common/Button';
import Modal from '../common/Modal';
import WalletForm from './WalletForm';

const WalletList = ({ wallets, onWalletCreated }) => {
  const [showCreateModal, setShowCreateModal] = useState(false);

  const handleCreateWallet = (walletData) => {
    // In a real app, this would call an API
    onWalletCreated(walletData);
    setShowCreateModal(false);
  };

  return (
    <div className="pb-16"> {/* Padding for bottom navbar */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">My Wallets</h2>
        <Button onClick={() => setShowCreateModal(true)}>
          + New Wallet
        </Button>
      </div>

      {wallets.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <p className="text-gray-600 mb-4">You don't have any wallets yet</p>
          <Button onClick={() => setShowCreateModal(true)}>
            Create Your First Wallet
          </Button>
        </div>
      ) : (
        <div className="space-y-4">
          {wallets.map((wallet) => (
            <WalletCard key={wallet.id} wallet={wallet} />
          ))}
        </div>
      )}

      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Wallet"
      >
        <WalletForm onSubmit={handleCreateWallet} />
      </Modal>
    </div>
  );
};

export default WalletList;