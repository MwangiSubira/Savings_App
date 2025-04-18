// frontend/src/components/dashboard/SavingsChart.jsx
import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SavingsChart = ({ wallets, className = '' }) => {
  // Sample data - in a real app, this would come from API
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const walletData = wallets.map(wallet => ({
    label: wallet.name,
    data: months.map(() => Math.floor(Math.random() * 50000) + 10000),
    borderColor: `#${Math.floor(Math.random()*16777215).toString(16)}`,
    tension: 0.1
  }));

  const data = {
    labels: months,
    datasets: walletData
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Savings Trend',
      },
    },
  };

  return (
    <div className={`bg-white rounded-xl shadow-md p-4 ${className}`}>
      <Line data={data} options={options} />
    </div>
  );
};

export default SavingsChart;