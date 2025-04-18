// frontend/src/pages/Wallets.jsx
import React from 'react';
import WalletList from '../../components/wallets/WalletList';
import useAuthRedirect from '../../hooks/useAuth';

const Wallets = () => {
  useAuthRedirect();
  const [wallets, setWallets] = useState([]);

  // In a real app, you would fetch wallets from API
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setWallets([
        { id: 1, name: 'Main Wallet', balance: 25000, lastDeposit: 5000, lastWithdrawal: 2000 },
        { id: 2, name: 'Savings', balance: 15000, lastDeposit: 3000, lastWithdrawal: 0 },
      ]);
    }, 500);
  }, []);

  const handleWalletCreated = (newWallet) => {
    setWallets([...wallets, { ...newWallet, id: Date.now(), balance: newWallet.initialBalance }]);
  };

  return (
    <div className="container mx-auto px-4 py-6">
      <WalletList wallets={wallets} onWalletCreated={handleWalletCreated} />
    </div>
  );
};

export default Wallets;