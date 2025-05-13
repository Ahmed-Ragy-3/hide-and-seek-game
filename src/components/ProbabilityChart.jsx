import React, { useContext } from 'react';
import GameContext from '../contexts/GameContext';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ProbabilityChart = () => {
  const { probabilities, playerRole } = useContext(GameContext);

  if (probabilities.length === 0) return null;

  const data = {
    labels: probabilities.map((_, i) => `Location ${i + 1}`),
    datasets: [
      {
        label: `Computer's ${playerRole} Probabilities`,
        data: probabilities,
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Optimal Strategy Probabilities',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
        title: {
          display: true,
          text: 'Probability',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Location',
        },
      },
    },
  };

  return (
    <div className="probability-chart">
      <Bar data={data} options={options} />
    </div>
  );
};

export default ProbabilityChart;