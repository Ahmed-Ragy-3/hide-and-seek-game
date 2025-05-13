import React, { useContext } from 'react';
import GameContext from '../contexts/GameContext';

const ResultsTable = () => {
  const { gameHistory } = useContext(GameContext);

  if (gameHistory.length === 0) return null;

  return (
    <div className="results-table">
      <h3>Game History</h3>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Round</th>
              <th>Your Move</th>
              <th>Computer Move</th>
              <th>Your Points</th>
              <th>Computer Points</th>
              <th>Cell Type</th>
            </tr>
          </thead>
          <tbody>
            {gameHistory.map((round, index) => (
              <tr key={`round-${index}`}>
                <td>{round.round}</td>
                <td>Location {round.playerMove + 1}</td>
                <td>Location {round.computerMove + 1}</td>
                <td className={round.playerPoints >= 0 ? 'positive' : 'negative'}>
                  {round.playerPoints}
                </td>
                <td className={round.computerPoints >= 0 ? 'positive' : 'negative'}>
                  {round.computerPoints}
                </td>
                <td>{round.worldType}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsTable;