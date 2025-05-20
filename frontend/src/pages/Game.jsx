import { useLocation } from 'react-router-dom';
import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa'; 
import Card from '../components/Card';
import styles from './Game.module.css';
import thefImage from '../assets/thef2.png'
import policeImage from '../assets/p2.png'
import greenImage from '../assets/green.png';
import yellowImage from '../assets/yellow.png';
import redImage from '../assets/red.png';
import PayoffModal from '../components/PayoffModal';
import StrategyToggle from '../components/StrategyToggle';
import Catch from '../assets/catch.png';

export default function Game() {
  const navigate = useNavigate();
  const location = useLocation();const { name, dimension, mode, n, m } = location.state || {};
  const [world, setWorld] = useState(location.state?.world || []);
  const [payoff, setPayoff] = useState(location.state?.payoff || []);
  const [hider_prob, setHiderProb] = useState(location.state?.hider_prob || []);
  const [seeker_prob, setSeekerProb] = useState(location.state?.seeker_prob || []);
  const gridRef = useRef(null);
  const [policeScore, setPoliceScore] = useState(0);
  const [thiefScore, setThiefScore] = useState(0);
  const [policeRounds, setPoliceRounds] = useState(0);
  const [thiefRounds, setThiefRounds] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [selectedStrategy, setSelectedStrategy] = useState('optimal');
  const [flippedCards, setFlippedCards] = useState(new Set());
  const [userSelectedIndex, setUserSelectedIndex] = useState(null);
  const [serverSelectedIndex, setServerSelectedIndex] = useState(null);
  // Convert to numbers
  const cols = parseInt(n, 10) || 1; // columns
  const rows = dimension === "2D" ? parseInt(m, 10) || 1 : 1; // rows
  const thiefBackImg = thefImage;
  const policeBackImg = policeImage;
  const thiefInPreson = Catch ;
  const defaultBackImg = ''; 


  // Set CSS variables for grid layout
  useEffect(() => {
    if (gridRef.current) {
      gridRef.current.style.setProperty('--cols', cols);
      gridRef.current.style.setProperty('--rows', rows);
    }
  }, [cols, rows]);

const handleReset = async () => {
  try {
    // 1. Reset frontend state
    setPoliceScore(0);
    setThiefScore(0);
    setPoliceRounds(0);
    setThiefRounds(0);
    setUserSelectedIndex(null);
    setServerSelectedIndex(null);
    setFlippedCards(new Set());

    // 2. Request new grid from backend
    const res = await fetch('http://localhost:5000/game', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        N: parseInt(n), // from location.state
        M: dimension === '2D' ? parseInt(m) : 1,
        role: mode === 'thief' ? 'hider' : 'seeker',
      }),
    });

    const data = await res.json();

    // 3. Update grid and game state
    if (data.world) {
      setWorld(data.world);
      setPayoff(data.payoff_matrix);
      setHiderProb(data.hider_prob);
      setSeekerProb(data.seeker_prob);
    }
  } catch (err) {
    console.error('Error during reset:', err);
  }
};


const handleCardClick = async (index) => {
  try {
    setUserSelectedIndex(index); 
    console.log({
    player_type: mode === 'thief' ? 'hider' : 'seeker',
    is_optimal: selectedStrategy === 'optimal'
    });
    const res = await fetch('http://localhost:5000/round', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        player_type: mode === 'thief' ? 'HIDER' : 'SEEKER',
        is_optimal: selectedStrategy === 'optimal'
      })
    });

    const data = await res.json();
    const [row, col] = data.move;
    const serverIndex = row * cols + col;
    let score;

    if (mode === 'thief') {
      score = payoff[index][serverIndex]; 
    } else {
      score = payoff[serverIndex][index]; 
    }
    setPoliceScore(prev => prev - score);
    setThiefScore(prev => prev + score);
    if (score < 0) {
      setPoliceRounds(prev => prev + 1);
    }
    else{
      setThiefRounds(prev => prev + 1);
    }
    console.log(serverIndex)
    console.log(index)
    console.log(score)

    setServerSelectedIndex(serverIndex);

    const allIndices = new Set(Array.from({ length: rows * cols }, (_, i) => i));
    setFlippedCards(allIndices);

    setTimeout(() => {
      setFlippedCards(new Set());
      setUserSelectedIndex(null);
      setServerSelectedIndex(null);
    }, 1000);
  } catch (err) {
    console.error('Error:', err);
  }
};

  return (
    <div className={styles.wrapper}>
                {showModal && (
            <PayoffModal
              payoff={payoff}
              hiderProb={hider_prob}
              seekerProb={seeker_prob}
              onClose={() => setShowModal(false)}
            />
          )}
      <button
        onClick={() => navigate('/')}
        className={styles.backButton}
        aria-label="Go back"
      >
        <FaArrowLeft size={20} />
      </button>
      <div className={styles.leftSection}>
        {(mode === 'thief' || mode === 'policeman') && (
          <div className={`${styles.imageContainer} ${styles.shake}`}>
            <img
              src={mode === 'thief' ? thefImage : policeImage}
              alt={mode}
            />
          </div>
        )}
        
        <div className={styles.scoreSection}>
          <div className={styles.scoreDisplay}>
            <div className={styles.scoreItem}>
              <span className={styles.scoreLabel}>Rounds</span>
              <span title='Police : Thief' className={styles.scoreValue}>{policeRounds} : {thiefRounds}</span>

            </div>
            <div className={styles.scoreItem}>
              <span className={styles.scoreLabel}>Score</span>
              <span  title='Police : Thief' className={styles.scoreValue}>{policeScore} : {thiefScore}</span>

            </div>
          </div>

          <button
            className={styles.showbutton}
            onClick={() => setShowModal(true)}
          >
            Show Data
          </button>
          <StrategyToggle selected={selectedStrategy} onChange={setSelectedStrategy} />
        </div>
      </div>

      <div className={styles.container}>
      <button className={styles.resetButton} onClick={handleReset}>
            Reset Game
      </button>
        <h1 className={styles.title}>Welcome {name} 😎</h1>

        <div className={styles.gridContainer}>
          <div ref={gridRef} className={styles.grid}>
          {Array.from({ length: rows * cols }).map((_, index) => {
            const rowIdx = Math.floor(index / cols);
            const colIdx = index % cols;
            const cellType = world?.[rowIdx]?.[colIdx];

            let img = '';
            switch (cellType) {
              case 'easy':
                img = greenImage; 
                break;
              case 'neutral':
                 img = yellowImage;
                break;
              case 'hard':
                img = redImage; 
                break;
              default:
                img = ''; 
            }
            return (
<Card
  key={`${rowIdx}-${colIdx}`}
  frontImage={img}
  frontText=""
backImage={
  index === userSelectedIndex && index === serverSelectedIndex
    ? thiefInPreson 
    : mode === 'thief'
      ? index === userSelectedIndex
        ? thiefBackImg
        : index === serverSelectedIndex
        ? policeBackImg
        : defaultBackImg
      : index === userSelectedIndex
      ? policeBackImg
      : index === serverSelectedIndex
      ? thiefBackImg
      : defaultBackImg
}
  isFlipped={flippedCards.has(index)}
  onClick={() => handleCardClick(index)}
/>
            );
          })}
          </div>
        </div>
      </div>
      
    </div>
  );
}