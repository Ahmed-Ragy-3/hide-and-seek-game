import React, { useContext } from 'react';
import GameContext from '../contexts/GameContext';

const GameControls = () => {
  const {
    worldSize,
    setWorldSize,
    playerRole,
    setPlayerRole,
    gameMode,
    setGameMode,
    is2D,
    setIs2D,
    proximityEnabled,
    setProximityEnabled,
    resetGame
  } = useContext(GameContext);

  const handleWorldSizeChange = (e) => {
    const size = parseInt(e.target.value);
    if (size >= 2 && size <= 10) {
      setWorldSize(size);
    }
  };

  const handleRoleSelect = (role) => {
    setPlayerRole(role);
  };

  const handleModeChange = (mode) => {
    setGameMode(mode);
  };

  return (
    <div className="game-controls">
      <div className="control-group">
        <label>World Size:</label>
        <input
          type="number"
          min="2"
          max="10"
          value={worldSize}
          onChange={handleWorldSizeChange}
          disabled={playerRole !== null}
        />
      </div>

      <div className="control-group">
        <label>Game Mode:</label>
        <div className="button-group">
          <button
            className={gameMode === 'interactive' ? 'active' : ''}
            onClick={() => handleModeChange('interactive')}
          >
            Interactive
          </button>
          <button
            className={gameMode === 'simulation' ? 'active' : ''}
            onClick={() => handleModeChange('simulation')}
          >
            Simulation
          </button>
        </div>
      </div>

      {gameMode === 'interactive' && (
        <div className="control-group">
          <label>Choose Role:</label>
          <div className="button-group">
            <button
              className={playerRole === 'hider' ? 'active' : ''}
              onClick={() => handleRoleSelect('hider')}
              disabled={playerRole !== null}
            >
              Hider
            </button>
            <button
              className={playerRole === 'seeker' ? 'active' : ''}
              onClick={() => handleRoleSelect('seeker')}
              disabled={playerRole !== null}
            >
              Seeker
            </button>
          </div>
        </div>
      )}

      <div className="control-group">
        <label>World Type:</label>
        <div className="button-group">
          <button
            className={is2D ? 'active' : ''}
            onClick={() => setIs2D(!is2D)}
          >
            {is2D ? '2D World' : '1D World'}
          </button>
        </div>
      </div>

      <div className="control-group">
        <label>Proximity Bonus:</label>
        <div className="button-group">
          <button
            className={proximityEnabled ? 'active' : ''}
            onClick={() => setProximityEnabled(!proximityEnabled)}
          >
            {proximityEnabled ? 'Enabled' : 'Disabled'}
          </button>
        </div>
      </div>

      <button className="reset-button" onClick={resetGame}>
        Reset Game
      </button>
    </div>
  );
};

export default GameControls;