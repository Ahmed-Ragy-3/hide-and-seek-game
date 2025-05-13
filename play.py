from game import Game
import numpy as np
import util as u
from lp_solver import solve_linear_program

class Play:
   def __init__(self, N, M=1, human=u.PLAYER.HIDER, mode=u.MODE.SIMULATION):
      self.human_role = human
      self.game = Game(N, M, human)
      self.mode = mode
      self.probabilities = np.zeros(self.game.M if human == u.PLAYER.HIDER else self.game.N)

   # def get_strategy_probabilities(self):
   #    # Get the payoff matrix from the game
   #    payoff_matrix = self.game.get_payoff_matrix()

   #    # Define the linear program to solve for mixed strategy probabilities
   #    num_strategies = len(payoff_matrix)
   #    c = [-1] * num_strategies  # Objective function coefficients (maximize)
   #    A_eq = [[1] * num_strategies]  # Sum of probabilities must equal 1
   #    b_eq = [1]
   #    bounds = [(0, 1) for _ in range(num_strategies)]  # Probabilities between 0 and 1

   #    # Solve the linear program
   #    probabilities = solve_linear_program(c, A_eq, b_eq, bounds)

   #    return probabilities

   def play(self):
      probabilities = self.get_strategy_probabilities()
      print("Optimal strategy probabilities:", probabilities)