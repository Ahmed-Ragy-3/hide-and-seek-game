import numpy as np
import random
import util as u
from tabulate import tabulate
class Game():
   def __init__(self, N, M=1, mode=u.MODE.INTERACTIVE, human_role=u.PLAYER.HIDER):
      assert N > 0, "N must be greater than 0"
      assert M > 0, "M must be greater than 0"
      self.N = N
      self.M = M
      
      self.mode = mode
      self.human_role = human_role
      self.turn = human_role

      # (hider, seeker)
      self.scores = (0, 0)
      self.rounds_won = (0, 0)

      self.__initialize()

   def __initialize(self):
      # world will be a 2D matrix of size M x N
      self.world = [[random.choice(list(u.PLACETYPE)) for _ in range(self.N)] for _ in range(self.M)]
      # Hider's score matrix: rows = hider, cols = seeker
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
            self.payoff_matrix[h][s] *= 4
            
            # proximity_score
            dis = abs(rs - rh) + abs(cs - ch)
            if dis == 1:
               self.payoff_matrix[h][s] *= 0.5
            
            elif dis == 2:
               self.payoff_matrix[h][s] *= 0.75
            
   def __distance(self, index1: int, index2: int) -> int:
      """
      Args:
         index1 (int): index of the hider in payoff matrix
         index2 (int): index of the seeker in payoff matrix
      Returns:
         int: distance between hider an seeker in the 2D world
      """
      # assert index1 != index2, "indices shouldn't be equal"
      rh, ch = self.__indices(index1)
      rs, cs = self.__indices(index2)

      return abs(rs - rh) + abs(cs - ch)
      # return max(diff_r, diff_c)


   def play_round(self):
      # Handle player actions and game logic
      # if human_role == 'hider':
      #    human_score = self.hider_score_matrix[human_move][computer_move]
      #    computer_score = -human_score
      # else:
      #    human_score = -self.hider_score_matrix[computer_move][human_move]
      #    computer_score = -human_score
      # return human_score, computer_score
      pass

   def reset(self):
      """
      Reset the game state.
      """
      self.turn = self.human_role
      self.scores = (0, 0)
      self.rounds_won = (0, 0)
      self.__initialize()

   def other(self, turn) -> u.PLAYER:
      assert turn in (u.PLAYER.HIDER, u.PLAYER.SEEKER), "Invalid player type"
      return u.PLAYER.HIDER if turn == u.PLAYER.SEEKER else u.PLAYER.SEEKER

   def __rand_indices(self) -> tuple:
      return random.randint(0, self.M - 1), random.randint(0, self.N - 1)
   
   def get_matrix(self) -> np.ndarray:
      return self.payoff_matrix

   def __indices(self, index: int) -> tuple:
      assert 0 <= index < (self.M * self.N), "Index out of bounds"
      return index // self.N, index % self.N


   def __str__(self) -> str:
      ret = f"Game Mode: {self.mode.value}\n"
      ret += f"Human Role: {self.human_role.value}\n"
      
      ret += f"\nWorld: {self.M} x {self.N}\n"
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
      ]
      ret += f"\nPayoff Matrix: {len(self.payoff_matrix)} x {len(self.payoff_matrix)}\n"
      ret += tabulate(table_data, headers=[""] + headers, tablefmt="grid")

      ret += f"\n\nScores:\n"
      ret += f"Hider: {self.scores[0]}, Seeker: {self.scores[1]}\n"
      ret += f"\nRounds Won: {self.rounds_won}\n"
      ret += f"Hider: {self.rounds_won[0]}, Seeker: {self.rounds_won[1]}\n"
      ret += f"\nCurrent Turn: {self.turn.value}\n"
      
      return ret