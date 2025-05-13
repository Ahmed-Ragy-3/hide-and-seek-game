import React from 'react';

const WorldTypeIndicator = ({ type }) => {
  const getTypeSymbol = () => {
    switch (type) {
      case 'hard': return '🪨';
      case 'easy': return '🌱';
      default: return '🟦';
    }
  };

  const getTypeTooltip = () => {
    switch (type) {
      case 'hard': return 'Hard place (better for hider)';
      case 'easy': return 'Easy place (better for seeker)';
      default: return 'Neutral place';
    }
  };

  return (
    <span className="type-indicator" title={getTypeTooltip()}>
      {getTypeSymbol()}
    </span>
  );
};

export default WorldTypeIndicator;