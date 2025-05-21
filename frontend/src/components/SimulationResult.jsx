// components/SimulationResult.js
import React from 'react';
import styles from './SimulationResult.module.css';

const SimulationResult = ({ moves, scores, roundsWon, onClose }) => {
  return (
    <div className={styles.overlay}>
      <div className={styles.container}>
        <button className={styles.closeButton} onClick={onClose}>✖</button>
<div
  style={{
    display: 'flex',
    gap: '50px',
    color: 'white',
    marginTop: '10px',
    justifyContent: 'center', 
  }}
>
  <p className={styles.stats}>
    <strong>Thief score:</strong> {scores[scores.length - 1][0]} &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>Police score:</strong> {scores[scores.length - 1][1]}
  </p>
  <p className={styles.stats}>
    <strong>Thief rounds won:</strong> {roundsWon[roundsWon.length - 1][0]} &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>Police rounds won:</strong> {roundsWon[roundsWon.length - 1][1]}
  </p>
</div>

<div className={styles.stepsContainer}>

  <div className={styles.stepRowHeader}>
    <div className={styles.roundNum}>Round</div>
    <div className={styles.moveBlock}>Thief Move</div>
    <div className={styles.moveBlock}>Police Move</div>
    <div className={styles.scoreBlock}>Score </div>
    <div className={styles.scoreBlock}>Rounds Won </div>
  </div>

  {moves.map((movePair, index) => {
    const [hiderMove, seekerMove] = movePair;
    const score = scores[index + 1] || [0, 0];
    const rounds = roundsWon[index + 1] || [0, 0];

    return (
      <div className={styles.stepRow} key={index}>
        <div className={styles.roundNum}>Round {index + 1}</div>
        <div className={styles.moveBlock}>
          <span className={styles.role}>Thief:</span> Row {hiderMove[0]}, Col {hiderMove[1]}
        </div>
        <div className={styles.moveBlock}>
          <span className={styles.role}>Police:</span> Row {seekerMove[0]}, Col {seekerMove[1]}
        </div>
        <div className={styles.scoreBlock}>
          <span className={styles.role}>Thief : Police →</span> {score[0]} : {score[1]}
        </div>
        <div className={styles.scoreBlock}>
          <span className={styles.role}>Thief : Police →</span> {rounds[0]} : {rounds[1]}
        </div>
      </div>
    );
  })}
</div>
      </div>
    </div>
  );
};

export default SimulationResult;
