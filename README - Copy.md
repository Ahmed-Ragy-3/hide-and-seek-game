# 🎯 Hide and Seek Game — Operations Research Assignment

A Python-based interactive game that simulates a strategic **hide-and-seek** scenario using **game theory** and **linear programming**. Designed for **Operations Research** coursework at Alexandria University.

## 📌 Assignment Overview

This project implements a strategic game between a **Hider** and a **Seeker** on a linear world. It includes:

- Mixed strategy generation using **Simplex (LP)**
- Interactive **GUI** for playing
- **Simulation mode** to run multiple rounds
- **Bonus features** like proximity scoring

---

## 🚀 Getting Started

### Requirements
- Python 3.7+
- `scipy`
- `numpy`

Install dependencies:

```bash
pip install numpy scipy
```

### Run the Game

```bash
python main.py
```

This will launch the GUI where you can choose your role (Hider or Seeker) and play interactively.

---

## 🎮 Game Description

* The world is a **linear set of N places**
* Each place is either:

  * `hard`: Seeker has lower chance of success
  * `neutral`: Equal scoring
  * `easy`: Seeker has higher chance of success
* The computer plays using an **optimal strategy** via Linear Programming (Simplex).

---

## 🧠 Game Theory + LP

This project formulates the Hide & Seek game as a **zero-sum game**:

* Hider: Maximizes their minimum payoff
* Seeker: Minimizes the Hider's payoff

We solve for the **optimal mixed strategy** using `scipy.optimize.linprog`.

---

## 🖥️ Features

✅ Choose role (Hider or Seeker)
✅ Randomly generated world types
✅ Score matrix with proximity effect
✅ Interactive GUI with scores and stats
✅ Simulation mode (100 rounds)
✅ Reset button

* ✅ **Proximity scoring**:

  * If the seeker is close, hider is penalized.
* 🔜 **2D world mode** (to be implemented)

---

## 📊 Simulation Example

Run 100 random rounds using:

```python
from simulation import run_simulation
run_simulation(N=4, role='hider', rounds=100)
```
