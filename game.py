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

   def start_game(self):
      print("Welcome to the game!")
      # self.initialize_game()
      while not self.game_over:
         self.play_round()

   def __initialize(self):
      # world will be a 2D matrix of size M x N
      self.world = [[random.choice(list(u.PLACETYPE)) for _ in range(self.N)] for _ in range(self.M)]
      # Hider's score matrix: rows = hider, cols = seeker
      total_size = self.M * self.N
      self.payoff_matrix = np.zeros((total_size, total_size)) 
      # for h in range(total_size):
      #    for s in range(total_size):
      #       place_type = self.world[s]  # The seeker determines the column
      #       hider_score = self.type_scores[place_type][0]
      #       if h == s:
      #          self.payoff_matrix[h][s] = hider_score  # Exact match
      #       else:
      #          self.payoff_matrix[h][s] = self.__proximity_score(h, s, hider_score)

   def __proximity_score(self, h, s, score):
      # Adjust score based on distance between hider and seeker
      distance = abs(h - s)
      if distance == 1:
         return score * 0.5
      
      elif distance == 2:
         return score * 0.75
      
      return score

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

   def other(self, turn) -> u.PLAYER:
      return u.HIDER if turn == u.SEEKER else u.SEEKER

   def __assign_scores__(self):
      """
      Assign a score to each place in the world for each player.
      """

   def __rand_indices__(self) -> tuple:
      return random.randint(0, self.M - 1), random.randint(0, self.N - 1)
   
   def get_matrix(self) -> np.ndarray:
      return self.payoff_matrix

   def indices(self, index: int) -> tuple:
      return index // self.N, index % self.N

   def __str__(self) -> str:
      ret = f"Game Mode: {self.mode.value}\n"
      ret += f"Human Role: {self.human_role.value}\n"
      ret += f"\nWorld: {self.M} x {self.N}\n"
      sep = "-" * 50 + "\n"
      ret += sep
      for row in self.world:
         ret += " "
         ret += " | ".join(cell.value.ljust(7) for cell in row) + f"\n{sep}"
      
      # Create a table of payoff matrix using tabulate
      headers = [f"H{u.sub(i + 1)}" for i in range(len(self.payoff_matrix))]
      row_labels = [f"S{u.sub(i + 1)}" for i in range(len(self.payoff_matrix))]
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