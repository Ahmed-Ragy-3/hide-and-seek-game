import React, { useContext } from 'react';
import GameContext from '../contexts/GameContext';

const GameMatrix = () => {
  const { scoreMatrix, playerRole } = useContext(GameContext);

  if (scoreMatrix.length === 0) return null;

  return (
    <div className="game-matrix">
      <h3>Payoff Matrix ({playerRole ? playerRole.charAt(0).toUpperCase() + playerRole.slice(1) : 'Player'}'s View)</h3>
      <div className="matrix-container">
        <table>
          <thead>
            <tr>
              <th></th>
              {scoreMatrix[0].map((_, i) => (
                <th key={`s${i}`}>S{i+1}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {scoreMatrix.map((row, i) => (
              <tr key={`h${i}`}>
                <th>H{i+1}</th>
                {row.map((cell, j) => (
                  <td key={`cell-${i}-${j}`}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="matrix-legend">
        <p><strong>H</strong> = Hider's choice, <strong>S</strong> = Seeker's choice</p>
        <p>Positive values indicate hider's payoff, negative values indicate seeker's payoff</p>
      </div>
    </div>
  );
};

export default GameMatrix;