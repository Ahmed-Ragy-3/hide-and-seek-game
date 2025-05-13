import React, { useContext, useEffect } from 'react';
import GameContext from '../contexts/GameContext';

const ThemeSelector = () => {
  const { theme, setTheme } = useContext(GameContext);

  const themes = [
    { id: 'light', name: 'Light' },
    { id: 'dark', name: 'Dark' },
    { id: 'ocean', name: 'Ocean' },
    { id: 'forest', name: 'Forest' }
  ];

  useEffect(() => {
    document.body.className = theme;
  }, [theme]);

  return (
    <div className="theme-selector">
      <select value={theme} onChange={(e) => setTheme(e.target.value)}>
        {themes.map((t) => (
          <option key={t.id} value={t.id}>{t.name} Theme</option>
        ))}
      </select>
    </div>
  );
};

export default ThemeSelector;