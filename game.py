import numpy as np
import random
import util as u
import lp_solver as lp
from tabulate import tabulate
class Game():
   def __init__(self, N, M=1):
      assert N > 0, "N must be greater than 0"
      assert M > 0, "M must be greater than 0"
      self.N = N
      self.M = M

      # self.computer_role = computer_role
      # (hider, seeker)
      # self.scores = (0, 0)
      # self.rounds_won = (0, 0)

      self.__initialize()
      self.hider_probabilities = None
      self.seeker_probabilities = None
      self.payoff_matrix = np.array([
         [-1, 0.5, 1, 1],
         [2, -1, 2, 2],
         [1, 0.5, -2, 1],
         [0.75, 2, 0.5, -1]
      ])

   def __initialize(self):
      self.world = [[random.choice(list(u.PLACETYPE)) for _ in range(self.N)] for _ in range(self.M)]
      
      total_size = self.M * self.N
      self.payoff_matrix = np.zeros((total_size, total_size))
      for h in range(total_size):
         for s in range(total_size):
            rh, ch = self.__indices(h)
            rs, cs = self.__indices(s)
            
            place_type = self.world[rh][ch]                 # The hardness of the place where the seeker is
            hider_score = u.type_scores[place_type][0]      # score of the hider when he is not found
            seeker_score = u.type_scores[place_type][1]     # score of the seeker when he finds hider
            
            self.payoff_matrix[h][s] = hider_score if h != s else -seeker_score
            # to prevent floats
            # self.payoff_matrix[h][s] *= 4
            
            # proximity_score
            dis = abs(rs - rh) + abs(cs - ch)
            if dis == 1:
               self.payoff_matrix[h][s] *= 0.5
            
            elif dis == 2:
               self.payoff_matrix[h][s] *= 0.75
            
            elif dis == 3:
               self.payoff_matrix[h][s] *= 0.25


   def play_round(self, player: u.PLAYER) -> tuple:
      """
      Determines the move (row, col) for the given player using their optimal mixed strategy.

      Returns:
         tuple: (row, col) index chosen based on strategy probabilities
      """
      assert player in (u.PLAYER.HIDER, u.PLAYER.SEEKER), "Invalid player type"

      if player == u.PLAYER.HIDER:
         if self.hider_probabilities is None:
            self.hider_probabilities = lp.solve_hider_strategy(self.payoff_matrix)
         probs = self.hider_probabilities

      else:  # player == u.PLAYER.SEEKER
         if self.seeker_probabilities is None:
            self.seeker_probabilities = lp.solve_seeker_strategy(self.payoff_matrix)
         probs = self.seeker_probabilities

      assert len(probs) == self.M * self.N, f"Expected {self.M * self.N} probabilities, got {len(probs)}"
      assert np.isclose(sum(probs), 1.0), f"Probabilities do not sum to 1: {probs}"
      assert all(0 <= p <= 1 for p in probs), f"Probabilities out of bounds: {probs}"

      index = np.random.choice(len(probs), p=probs)
      return self.__indices(index)

   
   def reset(self):
      """
      Reset the game state.
      """
      # self.scores = (0, 0)
      # self.rounds_won = (0, 0)
      self.__initialize()

   def other(self, turn) -> u.PLAYER:
      assert turn in (u.PLAYER.HIDER, u.PLAYER.SEEKER), "Invalid player type"
      return u.PLAYER.HIDER if turn == u.PLAYER.SEEKER else u.PLAYER.SEEKER

   def get_payoff_matrix(self) -> np.ndarray:
      return self.payoff_matrix
   
   def get_probabilties(self) -> np.ndarray:
      return self.probabilities

   def __indices(self, index: int) -> tuple:
      assert 0 <= index < (self.M * self.N), "Index out of bounds"
      return index // self.N, index % self.N

   def __str__(self) -> str:
      # ret = f"Computer Role: {self.computer_role.value}\n"
      
      ret = f"\nWorld: {self.M} x {self.N}\n"
      sep = "-" * (10 * self.N) + "\n"
      ret += sep
      for row in self.world:
         ret += " "
         ret += " | ".join(cell.value.ljust(7) for cell in row) + f"\n{sep}"
      
      # Create a table of payoff matrix using tabulate
      headers = [f"S{u.sub(i + 1)}" for i in range(len(self.payoff_matrix))]
      row_labels = [f"H{u.sub(i + 1)}" for i in range(len(self.payoff_matrix))]
      table_data = [
         [row_labels[i]] + list(map(str, row)) for i, row in enumerate(self.payoff_matrix)
         # [p for p in self.probabilities]
      ]
      
      ret += f"\nPayoff Matrix: {len(self.payoff_matrix)} x {len(self.payoff_matrix)}\n"
      ret += tabulate(table_data, headers=[""] + headers, tablefmt="grid")

      if self.hider_probabilities is not None:
         ret += f"\n\nProbabilities of hider:\n"
         ret += f"{self.hider_probabilities[:len(self.hider_probabilities)]}\n"

      if self.seeker_probabilities is not None:
         ret += f"\n\nProbabilities of seeker:\n"
         ret += f"{self.seeker_probabilities[:len(self.seeker_probabilities)]}\n"

      # ret += f"\n\nScores:\n"
      # # ret += f"Hider: {self.scores[0]}, Seeker: {self.scores[1]}\n"
      # ret += f"\nRounds Won: {self.rounds_won}\n"
      # # ret += f"Hider: {self.rounds_won[0]}, Seeker: {self.rounds_won[1]}\n"
      # ret += f"\nCurrent Turn: {self.turn.value}\n"
      
      return ret