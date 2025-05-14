import numpy as np
import random
import util as u
import lp_solver as lp
from tabulate import tabulate
class Game():
   def __init__(self, N, M=1, computer_role=u.PLAYER.HIDER):
      assert N > 0, "N must be greater than 0"
      assert M > 0, "M must be greater than 0"
      self.N = N
      self.M = M

      self.computer_role = computer_role
      # (hider, seeker)
      # self.scores = (0, 0)
      # self.rounds_won = (0, 0)

      self.__initialize()
      # self.__solve_probabilities()

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
            
   def __solve_probabilities(self):
      # Solve for the optimal mixed strategy for the hider (maximize minimum gain)
      self.probabilities = lp.solve_hider_strategy(self.payoff_matrix) if self.computer_role == u.PLAYER.HIDER \
                      else lp.solve_seeker_strategy(self.payoff_matrix)

      assert len(self.probabilities) == (self.M * self.N), "Probabilities length mismatch"
      assert np.isclose(sum(self.probabilities), 1.0), "Probabilities do not sum to 1"
      assert all(0 <= p <= 1 for p in self.probabilities), "Probabilities out of bounds"


   def play_round(self) -> tuple:
      """
      Returns:
          int, int: indices of which the computer should play
      """
      index = np.random.choice(len(self.probabilities), p=self.probabilities)
      row, col = self.__indices(index)
      return row, col
   
   def reset(self):
      """
      Reset the game state.
      """
      # self.scores = (0, 0)
      # self.rounds_won = (0, 0)
      self.__initialize()
      self.__solve_probabilities()

   # def other(self, turn) -> u.PLAYER:
   #    assert turn in (u.PLAYER.HIDER, u.PLAYER.SEEKER), "Invalid player type"
   #    return u.PLAYER.HIDER if turn == u.PLAYER.SEEKER else u.PLAYER.SEEKER

   def get_payoff_matrix(self) -> np.ndarray:
      return self.payoff_matrix
   
   def get_probabilties(self) -> np.ndarray:
      return self.probabilities

   def __indices(self, index: int) -> tuple:
      assert 0 <= index < (self.M * self.N), "Index out of bounds"
      return index // self.N, index % self.N

   def __str__(self) -> str:
      ret = f"Computer Role: {self.computer_role.value}\n"
      
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

      # ret += f"\n\nProbabilities of {self.computer_role.value}:\n"
      # ret += f"{self.probabilities[:len(self.probabilities)]}\n"

      # ret += f"\n\nScores:\n"
      # # ret += f"Hider: {self.scores[0]}, Seeker: {self.scores[1]}\n"
      # ret += f"\nRounds Won: {self.rounds_won}\n"
      # # ret += f"Hider: {self.rounds_won[0]}, Seeker: {self.rounds_won[1]}\n"
      # ret += f"\nCurrent Turn: {self.turn.value}\n"
      
      return ret