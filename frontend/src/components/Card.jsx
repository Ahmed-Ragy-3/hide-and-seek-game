import React, { useEffect, useRef, useState } from 'react';
import styles from './Card.module.css';

const Card = ({ frontImage, frontText, backImage, isFlipped, onClick }) => {
  const wrapperRef = useRef(null);
  const [size, setSize] = useState(0);

  useEffect(() => {
    const updateSize = () => {
      if (wrapperRef.current) {
        const { clientWidth, clientHeight } = wrapperRef.current;
        const minSize = Math.min(clientWidth, clientHeight);
        setSize(minSize);
      }
    };

    updateSize();
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  return (
    <div ref={wrapperRef} className={styles['card-wrapper']}>
      <div
        className={styles.card}
        onClick={onClick}
        style={{ width: size, height: size }}
      >
        <div
          className={`${styles['card-inner']} ${isFlipped ? styles.flipped : ''}`}
        >
          <div
            className={styles['card-front']}
            style={{
              backgroundImage: `url(${frontImage})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }}
          >
            <span className={styles['card-text']}>{frontText}</span>
          </div>
          <div className={styles['card-back']}>
            {backImage ? (
              <img
                src={backImage}
                alt="Card Back"
                className={styles['card-image']}
              />
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Card;
