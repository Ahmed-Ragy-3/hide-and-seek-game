import React, { useState } from 'react';
import styles from './StrategyToggle.module.css';

export default function StrategyToggle({ selected, onChange }) {
  return (
    <div className={styles.toggleWrapper}>
      <div className={styles.toggle}>
        <div className={`${styles.slider} ${selected === 'optimal' ? styles.left : styles.right}`} />
        <label className={styles.option}>
          <input
            type="radio"
            name="strategy"
            value="optimal"
            checked={selected === 'optimal'}
            onChange={() => onChange('optimal')}
          />
          Optimal
        </label>
        <label className={styles.option}>
          <input
            type="radio"
            name="strategy"
            value="random"
            checked={selected === 'random'}
            onChange={() => onChange('random')}
          />
          Random
        </label>
      </div>
    </div>
  );
}
