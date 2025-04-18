// frontend/src/components/wallets/WalletCard.jsx
import React, { useState } from 'react';
import Button from '../common/Button';
import Modal from '../common/Modal';
import DepositForm from './DepositForm';
import WithdrawForm from './WithdrawForm';

const WalletCard = ({ wallet }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [showDepositModal, setShowDepositModal] = useState(false);
  const [showWithdrawModal, setShowWithdrawModal] = useState(false);

  return (
    <div className="bg-white rounded-xl shadow-md p-4 mb-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="font-bold text-lg">{wallet.name || 'Primary Wallet'}</h3>
          <p className="text-gray-600 text-sm">Balance: KES {wallet.balance?.toLocaleString() || '0'}</p>
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
          <div className="flex justify-between py-2 border-b">
            <span>Last Deposit</span>
            <span className="font-medium">KES {wallet.lastDeposit?.toLocaleString() || '0'}</span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span>Last Withdrawal</span>
            <span className="font-medium">KES {wallet.lastWithdrawal?.toLocaleString() || '0'}</span>
          </div>
          <div className="flex justify-between py-2">
            <span>Created On</span>
            <span className="font-medium">{wallet.createdAt || 'N/A'}</span>
          </div>

          <div className="flex gap-2 mt-4">
            <Button 
              size="small" 
              className="flex-1"
              onClick={() => setShowDepositModal(true)}
            >
              Deposit
            </Button>
            <Button 
              size="small" 
              variant="secondary" 
              className="flex-1"
              onClick={() => setShowWithdrawModal(true)}
            >
              Withdraw
            </Button>
          </div>
        </div>
      )}

      <Modal 
        isOpen={showDepositModal} 
        onClose={() => setShowDepositModal(false)}
        title="Deposit Funds"
      >
        <DepositForm 
          walletId={wallet.id} 
          onSuccess={() => {
            setShowDepositModal(false);
            setShowDetails(true);
          }} 
        />
      </Modal>

      <Modal 
        isOpen={showWithdrawModal} 
        onClose={() => setShowWithdrawModal(false)}
        title="Withdraw Funds"
      >
        <WithdrawForm 
          walletId={wallet.id}
          currentBalance={wallet.balance}
          onSuccess={() => {
            setShowWithdrawModal(false);
            setShowDetails(true);
          }}
        />
      </Modal>
    </div>
  );
};

export default WalletCard;