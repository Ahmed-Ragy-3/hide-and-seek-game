import React, { useContext } from 'react';
import GameContext from '../contexts/GameContext';
import WorldTypeIndicator from './WorldTypeIndicator';

const GameBoard = () => {
  const {
    worldSize,
    is2D,
    worldType,
    playerRole,
    playerChoice,
    computerChoice,
    playRound,
    gameMode,
    roundsPlayed
  } = useContext(GameContext);

  const handleCellClick = (index) => {
    if (playerRole && gameMode === 'interactive') {
      playRound(index);
    }
  };

  const renderCell = (index) => {
    const isPlayerChoice = playerChoice === index;
    const isComputerChoice = computerChoice === index;
    const type = worldType[index];
    
    let className = 'cell';
    if (type) className += ` ${type}`;
    if (isPlayerChoice) className += ' player-choice';
    if (isComputerChoice) className += ' computer-choice';
    
    return (
      <div
        key={index}
        className={className}
        onClick={() => handleCellClick(index)}
      >
        <WorldTypeIndicator type={type} />
        {isPlayerChoice && <div className="choice-label">You</div>}
        {isComputerChoice && <div className="choice-label">Computer</div>}
      </div>
    );
  };

  if (is2D) {
    const gridSize = Math.sqrt(worldSize * worldSize);
    return (
      <div className="game-board-2d">
        <h3>World Grid</h3>
        <div className="grid-container" style={{ 
          gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
          gridTemplateRows: `repeat(${gridSize}, 1fr)`
        }}>
          {Array(worldSize * worldSize).fill().map((_, i) => renderCell(i))}
        </div>
      </div>
    );
  }

  return (
    <div className="game-board-linear">
      <h3>World</h3>
      <div className="linear-container">
        {Array(worldSize).fill().map((_, i) => renderCell(i))}
      </div>
    </div>
  );
};

export default GameBoard;