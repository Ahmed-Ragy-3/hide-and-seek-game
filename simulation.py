import random
import numpy as np
from game import Game
from lp_solver import solve_hider_strategy, solve_seeker_strategy

def run_simulation(N, role, rounds=100):
   # Run multiple game rounds with random player moves and optimal computer moves
   player_score = 0
   computer_score = 0

   for _ in range(rounds):
      game = Game(N)
      matrix = game.get_matrix()

      if role == 'hider':
         player_move = random.randint(0, N - 1)  # Random move for player
         strategy = solve_seeker_strategy(matrix)  # Optimal move for computer
         computer_move = np.random.choice(range(N), p=strategy)
      else:
         strategy = solve_hider_strategy(matrix)
         computer_move = np.random.choice(range(N), p=strategy)
         player_move = random.randint(0, N - 1)

      ps, cs = game.play_round(role, player_move, computer_move)
      player_score += ps
      computer_score += cs

   return player_score, computer_score