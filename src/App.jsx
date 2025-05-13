import React from 'react';
import { GameProvider } from './contexts/GameContext';
import GameControls from './components/GameControls';
import GameBoard from './components/GameBoard';
import GameInfo from './components/GameInfo';
import ResultsTable from './components/ResultsTable';
import ProbabilityChart from './components/ProbabilityChart';
import GameMatrix from './components/GameMatrix';
import ThemeSelector from './components/ThemeSelector';
import './styles/lightTheme.css';

function App() {
  return (
    <GameProvider>
      <div className="app-container">
        <ThemeSelector />
        <h1>Hide & Seek Game</h1>
        <div className="game-container">
          <div className="left-panel">
            <GameControls />
            <GameBoard />
            <GameInfo />
          </div>
          <div className="right-panel">
            <ProbabilityChart />
            <GameMatrix />
            <ResultsTable />
          </div>
        </div>
      </div>
    </GameProvider>
  );
}

export default App;