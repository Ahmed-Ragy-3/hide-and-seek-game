import numpy as np
import random
import util as u
class Game():
   def __init__(self, N, M=1, mode=u.MODE.INTERACTIVE, human=u.PLAYER.HIDER):
      self.N = N
      self.M = M
      self.turn = None
      self.game_over = False
      self.hider_score = 0
      self.seeker_score = 0
      
      self.hider_rounds_won = 0
      self.seeker_rounds_won = 0

      self.__initialize()

   def start_game(self):
      print("Welcome to the game!")
      # self.initialize_game()
      while not self.game_over:
         self.play_turn()

   def __initialize(self):
      # world will be a 2D matrix of size M x N
      self.world = [[random.choice(list(u.PLACETYPE)) for _ in range(self.N)] for _ in range(self.M)]
      # Hider's score matrix: rows = hider, cols = seeker
      total_size = self.M * self.N
      self.payoff_matrix = np.zeros((total_size, total_size)) 
      for h in range(total_size):
         for s in range(total_size):
            place_type = self.world[s]  # The seeker determines the column
            hider_score = self.type_scores[place_type][0]
            if h == s:
               self.payoff_matrix[h][s] = hider_score  # Exact match
            else:
               self.payoff_matrix[h][s] = self.__proximity_score(h, s, hider_score)

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

   def __rand_index__(self) -> tuple:
      return random.randint(0, self.M - 1), random.randint(0, self.N - 1)
   
   def get_matrix(self) -> np.ndarray:
      return self.payoff_matrix