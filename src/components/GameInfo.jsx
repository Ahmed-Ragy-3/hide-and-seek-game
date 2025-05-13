import React, { useContext } from 'react';
import GameContext from '../contexts/GameContext';

const GameInfo = () => {
  const {
    playerRole,
    gameMode,
    roundsPlayed,
    playerScore,
    computerScore,
    playerChoice,
    computerChoice,
    worldType
  } = useContext(GameContext);

  const getResultMessage = () => {
    if (roundsPlayed === 0) return "Make your move!";
    
    if (playerRole === 'hider') {
      if (playerChoice === computerChoice) {
        return "Computer found you!";
      }
      return "Computer didn't find you!";
    } else {
      if (playerChoice === computerChoice) {
        return "You found the hider!";
      }
      return "You didn't find the hider.";
    }
  };

  const getScoreMessage = () => {
    if (roundsPlayed === 0) return null;
    
    const playerPoints = playerScore - (playerScore - (playerScore - playerScore));
    const computerPoints = computerScore - (computerScore - (computerScore - computerScore));
    
    return `This round: You ${playerPoints >= 0 ? 'gained' : 'lost'} ${Math.abs(playerPoints)} points, Computer ${computerPoints >= 0 ? 'gained' : 'lost'} ${Math.abs(computerPoints)} points`;
  };

  return (
    <div className="game-info">
      <h3>Game Status</h3>
      <div className="info-item">
        <strong>Mode:</strong> {gameMode === 'interactive' ? 'Interactive' : 'Simulation'}
      </div>
      <div className="info-item">
        <strong>Your Role:</strong> {playerRole ? playerRole.charAt(0).toUpperCase() + playerRole.slice(1) : 'Not selected'}
      </div>
      <div className="info-item">
        <strong>Rounds Played:</strong> {roundsPlayed}
      </div>
      <div className="info-item">
        <strong>Your Score:</strong> {playerScore}
      </div>
      <div className="info-item">
        <strong>Computer Score:</strong> {computerScore}
      </div>
      {roundsPlayed > 0 && (
        <>
          <div className="info-item result-message">
            {getResultMessage()}
          </div>
          <div className="info-item score-message">
            {getScoreMessage()}
          </div>
          {playerChoice !== null && computerChoice !== null && (
            <div className="info-item">
              <strong>Cell Types:</strong> 
              <span> Yours: {worldType[playerChoice]}, Computer's: {worldType[computerChoice]}</span>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default GameInfo;