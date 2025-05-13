import React, { createContext, useState, useEffect } from 'react';
import { solveLP } from '../services/api';

const GameContext = createContext();

export const GameProvider = ({ children }) => {
  const [worldSize, setWorldSize] = useState(4);
  const [playerRole, setPlayerRole] = useState(null);
  const [gameMode, setGameMode] = useState('interactive');
  const [worldType, setWorldType] = useState([]);
  const [playerChoice, setPlayerChoice] = useState(null);
  const [computerChoice, setComputerChoice] = useState(null);
  const [scoreMatrix, setScoreMatrix] = useState([]);
  const [probabilities, setProbabilities] = useState([]);
  const [gameHistory, setGameHistory] = useState([]);
  const [theme, setTheme] = useState('light');
  const [is2D, setIs2D] = useState(false);
  const [proximityEnabled, setProximityEnabled] = useState(false);
  const [roundsPlayed, setRoundsPlayed] = useState(0);
  const [playerScore, setPlayerScore] = useState(0);
  const [computerScore, setComputerScore] = useState(0);

  // Initialize game world
  const initializeWorld = () => {
    const types = Array(worldSize * (is2D ? worldSize : 1)).fill(0).map(() => {
      const rand = Math.random();
      if (rand < 0.33) return 'hard';
      if (rand < 0.66) return 'neutral';
      return 'easy';
    });
    
    setWorldType(types);
    generateScoreMatrix(types);
  };

  // Generate score matrix based on world types
  const generateScoreMatrix = (types) => {
    const matrix = [];
    for (let h = 0; h < types.length; h++) {
      const row = [];
      for (let s = 0; s < types.length; s++) {
        if (h === s) {
          // Seeker found the hider
          row.push(getScoreForFound(types[h], false));
        } else {
          // Seeker didn't find the hider
          row.push(getScoreForNotFound(types[h], h, s));
        }
      }
      matrix.push(row);
    }
    setScoreMatrix(matrix);
  };

  const getScoreForFound = (type, isPlayer) => {
    switch (type) {
      case 'hard': return isPlayer ? -3 : 3;
      case 'easy': return isPlayer ? 2 : -1;
      default: return isPlayer ? -1 : 1;
    }
  };

  const getScoreForNotFound = (type, hiderPos, seekerPos) => {
    let baseScore;
    switch (type) {
      case 'hard': baseScore = 1; break;
      case 'easy': baseScore = 2; break;
      default: baseScore = 1;
    }
    
    if (proximityEnabled) {
      const distance = Math.abs(hiderPos - seekerPos);
      if (distance === 1) return baseScore * 0.5;
      if (distance === 2) return baseScore * 0.75;
    }
    
    return baseScore;
  };

  // Calculate computer probabilities using LP solver
  const calculateProbabilities = async () => {
    try {
      const response = await solveLP(scoreMatrix, playerRole);
      setProbabilities(response.probabilities);
    } catch (error) {
      console.error('Error calculating probabilities:', error);
    }
  };

  // Make computer move based on probabilities
  const makeComputerMove = () => {
    if (probabilities.length === 0) return null;
    
    const rand = Math.random();
    let cumulative = 0;
    for (let i = 0; i < probabilities.length; i++) {
      cumulative += probabilities[i];
      if (rand < cumulative) return i;
    }
    return probabilities.length - 1;
  };

  // Play a round of the game
  const playRound = (playerMove) => {
    if (!playerRole) return;
    
    const computerMove = makeComputerMove();
    setPlayerChoice(playerMove);
    setComputerChoice(computerMove);
    
    let playerPoints = 0;
    let computerPoints = 0;
    
    if (playerRole === 'hider') {
      playerPoints = scoreMatrix[playerMove][computerMove];
      computerPoints = -playerPoints;
    } else {
      computerPoints = scoreMatrix[computerMove][playerMove];
      playerPoints = -computerPoints;
    }
    
    setPlayerScore(prev => prev + playerPoints);
    setComputerScore(prev => prev + computerPoints);
    setRoundsPlayed(prev => prev + 1);
    
    setGameHistory(prev => [
      ...prev,
      {
        round: prev.length + 1,
        playerMove,
        computerMove,
        playerPoints,
        computerPoints,
        playerRole,
        worldType: worldType[playerMove]
      }
    ]);
  };

  // Reset game state
  const resetGame = () => {
    setPlayerRole(null);
    setPlayerChoice(null);
    setComputerChoice(null);
    setGameHistory([]);
    setRoundsPlayed(0);
    setPlayerScore(0);
    setComputerScore(0);
    initializeWorld();
  };

  // Effect to initialize world when parameters change
  useEffect(() => {
    if (worldSize) {
      initializeWorld();
    }
  }, [worldSize, is2D, proximityEnabled]);

  // Effect to calculate probabilities when matrix or role changes
  useEffect(() => {
    if (scoreMatrix.length > 0 && playerRole) {
      calculateProbabilities();
    }
  }, [scoreMatrix, playerRole]);

  return (
    <GameContext.Provider value={{
      worldSize,
      setWorldSize,
      playerRole,
      setPlayerRole,
      gameMode,
      setGameMode,
      worldType,
      playerChoice,
      computerChoice,
      scoreMatrix,
      probabilities,
      gameHistory,
      theme,
      setTheme,
      is2D,
      setIs2D,
      proximityEnabled,
      setProximityEnabled,
      roundsPlayed,
      playerScore,
      computerScore,
      playRound,
      resetGame
    }}>
      {children}
    </GameContext.Provider>
  );
};

export default GameContext;