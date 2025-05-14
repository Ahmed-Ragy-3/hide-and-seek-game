import random
import numpy as np
from game import Game
from lp_solver import solve_hider_strategy, solve_seeker_strategy

def simulate(N, M=1, rounds=100):
   # Run multiple game rounds with random player moves and optimal computer moves
   player_score = 0
   computer_score = 0
   game = Game(N, M)

   for _ in range(rounds):
      matrix = game.get_matrix()
      # ps, cs = game.play_round(role)

      # if role == 'hider':
      # else:

      # player_score += ps
      # computer_score += cs

   return player_score, computer_score