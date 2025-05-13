export const solveLP = async (matrix, role) => {
  // In a real implementation, this would call a backend API
  // For now, we'll simulate it with a simple algorithm
  
  // For hider: maximize minimum gain (maximin)
  // For seeker: minimize maximum loss (minimax)
  
  const numStrategies = matrix.length;
  
  if (role === 'hider') {
    // Find strategy with highest minimum payoff
    const strategyPayoffs = matrix.map(row => Math.min(...row));
    const maxMin = Math.max(...strategyPayoffs);
    const optimalStrategies = strategyPayoffs.map((val, idx) => 
      val === maxMin ? idx : -1
    ).filter(idx => idx !== -1);
    
    // Equal probability for all optimal strategies
    const probabilities = Array(numStrategies).fill(0);
    optimalStrategies.forEach(idx => {
      probabilities[idx] = 1 / optimalStrategies.length;
    });
    
    return { probabilities };
  } else {
    // For seeker, we need to consider the negative of the matrix (since it's zero-sum)
    const negMatrix = matrix.map(row => row.map(val => -val));
    
    // Find strategy with lowest maximum payoff (from seeker's perspective)
    const strategyPayoffs = negMatrix[0].map((_, colIdx) => 
      Math.max(...negMatrix.map(row => row[colIdx]))
    );
    const minMax = Math.min(...strategyPayoffs);
    const optimalStrategies = strategyPayoffs.map((val, idx) => 
      val === minMax ? idx : -1
    ).filter(idx => idx !== -1);
    
    // Equal probability for all optimal strategies
    const probabilities = Array(numStrategies).fill(0);
    optimalStrategies.forEach(idx => {
      probabilities[idx] = 1 / optimalStrategies.length;
    });
    
    return { probabilities };
  }
};

export const simulateGame = async (numRounds, worldSize, is2D, proximityEnabled) => {
  // Simulate 100 rounds of random play
  const results = {
    playerWins: 0,
    computerWins: 0,
    ties: 0,
    playerScore: 0,
    computerScore: 0,
    rounds: []
  };
  
  // Initialize a random world
  const types = Array(worldSize * (is2D ? worldSize : 1)).fill(0).map(() => {
    const rand = Math.random();
    if (rand < 0.33) return 'hard';
    if (rand < 0.66) return 'neutral';
    return 'easy';
  });
  
  // Generate score matrix
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

  const matrix = [];
  for (let h = 0; h < types.length; h++) {
    const row = [];
    for (let s = 0; s < types.length; s++) {
      if (h === s) {
        row.push(getScoreForFound(types[h], false));
      } else {
        row.push(getScoreForNotFound(types[h], h, s));
      }
    }
    matrix.push(row);
  }
  
  // Randomly assign roles for each round
  for (let i = 0; i < numRounds; i++) {
    const playerRole = Math.random() < 0.5 ? 'hider' : 'seeker';
    const playerMove = Math.floor(Math.random() * types.length);
    
    // Calculate computer probabilities
    const { probabilities } = await solveLP(matrix, playerRole === 'hider' ? 'seeker' : 'hider');
    
    // Make computer move
    const rand = Math.random();
    let cumulative = 0;
    let computerMove = 0;
    for (let j = 0; j < probabilities.length; j++) {
      cumulative += probabilities[j];
      if (rand < cumulative) {
        computerMove = j;
        break;
      }
    }
    
    // Calculate scores
    let playerPoints = 0;
    let computerPoints = 0;
    
    if (playerRole === 'hider') {
      playerPoints = matrix[playerMove][computerMove];
      computerPoints = -playerPoints;
    } else {
      computerPoints = matrix[computerMove][playerMove];
      playerPoints = -computerPoints;
    }
    
    // Update results
    results.playerScore += playerPoints;
    results.computerScore += computerPoints;
    
    if (playerPoints > computerPoints) results.playerWins++;
    else if (computerPoints > playerPoints) results.computerWins++;
    else results.ties++;
    
    results.rounds.push({
      round: i + 1,
      playerRole,
      playerMove,
      computerMove,
      playerPoints,
      computerPoints,
      worldType: types[playerMove]
    });
  }
  
  return results;
};