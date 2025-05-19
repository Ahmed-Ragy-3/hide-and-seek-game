import React, { useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer
} from 'recharts';
import styles from './PayoffModal.module.css';

export default function PayoffModal({ payoff, hiderProb, seekerProb, onClose }) {
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, []);

  useEffect(() => {
    const handleEscKey = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleEscKey);
    return () => {
      window.removeEventListener('keydown', handleEscKey);
    };
  }, [onClose]);

  const handleOverlayClick = (e) => {
    if (e.target.className === styles.modalOverlay) {
      onClose();
    }
  };

  // Prepare data for Recharts
  const hiderData = hiderProb?.map((p, i) => ({ name: `H${i + 1}`, prob: p }));
  const seekerData = seekerProb?.map((p, i) => ({ name: `S${i + 1}`, prob: p }));

  return (
    <div className={styles.modalOverlay} onClick={handleOverlayClick}>
      <div className={styles.modalContent}>
        <h2>Payoff Matrix</h2>
<table className={styles.table}>
        <thead>
            <tr>
            <th></th> 
            {payoff?.[0]?.map((_, j) => (
                <th key={`col-${j}`}>S{j + 1}</th>
            ))}
            </tr>
        </thead>
        <tbody>
            {payoff?.map((row, i) => (
            <tr key={`row-${i}`}>
                <th>H{i + 1}</th>
                {row.map((cell, j) => (
                <td key={`cell-${i}-${j}`}>{cell}</td>
                ))}
            </tr>
            ))}
        </tbody>
        </table>

        <h2>Thief Probabilities</h2>
        <div className={styles.chartContainer}>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={hiderData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name"  stroke="#fff" />
              <YAxis domain={[0, 1]} stroke="#fff" />
              <Tooltip />
              <Bar dataKey="prob" fill="#aaadaa" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <h2>Police Probabilities</h2>
        <div className={styles.chartContainer}>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={seekerData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name"  stroke="#fff" />
              <YAxis domain={[0, 1]}  stroke="#fff" />
              <Tooltip />
              <Bar dataKey="prob" fill="#3d62a1" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <button onClick={onClose} className={styles.closeButton}>
          Close
        </button>
      </div>
    </div>
  );
}
