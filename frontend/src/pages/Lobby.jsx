import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Lobby.module.css";
import thefImage from '../assets/th_run.png'
import policeImage from '../assets/p_run.png'


export default function Lobby() {
  const [name, setName] = useState("");
  const [dimension, setDimension] = useState("1D");
  const [mode, setMode] = useState("policeman");
  const [n, setN] = useState("");
  const [m, setM] = useState("");
  const navigate = useNavigate();

const handleStart = async () => {
  const requestBody = {
    N: parseInt(n),
    M: dimension === "2D" ? parseInt(m) : 1,
    role: mode === "thief" ? "hider" : mode === "policeman" ? "seeker" : "simulation"
  };

  try {
    const response = await fetch('http://localhost:5000/game', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    const data = await response.json();

    if (!response.ok) {
      alert("Error: " + data.error);
      return;
    }
    console.log("Game created:", data);
    navigate('/game', {
      state: {
        name,
        dimension,
        mode,
        n,
        m,
        world: data.world,
        payoff:data.payoff_matrix,
        hider_prob:data.hider_prob,
        seeker_prob:data.seeker_prob,
      }
    });
  } catch (error) {
    console.error("Failed to start game:", error);
    alert("Failed to connect to server.");
  }
};
  

  return (
     <div className={styles.wrapper}>
      <div className={`${styles.imageContainer} ${styles.shake}`}>
       <img src={thefImage} alt="description" />
      </div>
    <div className={styles.container}>
      <h1 className={styles.title}>Amsk 7ramy</h1>

      <label className={styles.label}>Name</label>
      <input
        className={styles.input}
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
      />
        <div>
            <div>
                <label className={styles.label}>Select Mode</label>
            </div>
            <select
            className={styles.select}
            value={mode}
            onChange={(e) => setMode(e.target.value)}
            >
            <option value="policeman">Policeman</option>
            <option value="thief">Thief</option>
            <option value="simulation">Simulation Mode</option>
            </select>
        </div>

      <div className={styles.optionGroup}>
        <p>Select Dimension:</p>
        <label className={styles.radioLabel}>
          <input
            type="radio"
            value="1D"
            checked={dimension === "1D"}
            onChange={(e) => setDimension(e.target.value)}
          />
          1D
        </label>
        <label className={styles.radioLabel}>
          <input
            type="radio"
            value="2D"
            checked={dimension === "2D"}
            onChange={(e) => setDimension(e.target.value)}
          />
          2D
        </label>
      </div>

      <div className={styles.optionGroup}>
        {dimension === "1D" && (
          <>
            <label className={styles.label}>Columns</label>
            <input
              className={styles.input}
              type="number"
              value={n}
              onChange={(e) => setN(e.target.value)}
              placeholder="Enter N"
              min={1}
            />
          </>
        )}
        {dimension === "2D" && (
          <>
            <label className={styles.label}>Columns</label>
            <input
              className={styles.input}
              type="number"
              value={n}
              onChange={(e) => setN(e.target.value)}
              placeholder="Enter N"
              min={1}
            />
            <label className={styles.label}>Rows</label>
            <input
              className={styles.input}
              type="number"
              value={m}
              onChange={(e) => setM(e.target.value)}
              placeholder="Enter M"
              min={1}
            />
          </>
        )}
      </div>
      <button
        className={styles.button}
        onClick={handleStart}
        disabled={!name || !n || (dimension === "2D" && !m)}
      >
        Start Game
      </button>
    </div>
       <div className={`${styles.imageContainer} ${styles.shake}`}>
          <img src={policeImage} alt="description" />
        </div>
     
    </div>
  );
}
