// frontend/src/components/wallets/TransactionHistory.jsx
import React from 'react';

const TransactionHistory = ({ transactions }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-4">
      <h3 className="font-bold text-lg mb-4">Transaction History</h3>
      
      {transactions.length === 0 ? (
        <p className="text-gray-500 text-center py-4">No transactions yet</p>
      ) : (
        <div className="space-y-3">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="flex justify-between items-center py-2 border-b">
              <div>
                <p className="font-medium">{transaction.description || 'Transaction'}</p>
                <p className="text-sm text-gray-500">
                  {new Date(transaction.date).toLocaleDateString()}
                </p>
              </div>
              <p className={`font-bold ${transaction.type === 'deposit' ? 'text-green-600' : 'text-red-600'}`}>
                {transaction.type === 'deposit' ? '+' : '-'} KES {transaction.amount.toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TransactionHistory;