import util as u
import numpy as np
from game import Game
import copy

def simulate(game: Game, is_optimal=True, rounds=100):
   # (hider, seeker)
   moves = []
   scores = [(0, 0)]
   rounds_won = [(0, 0)]
   payoff = game.get_payoff_matrix()
   print(is_optimal)

   if is_optimal:
      play = game.play_optimal
   else:
      play = lambda player=None: game.play_random()

   for _ in range(rounds):
      cur_scores: tuple = copy.copy(scores[len(scores) - 1])
      cur_rounds_won: tuple = copy.copy(rounds_won[len(rounds_won) - 1])
      
      player1_move = play(player=u.PLAYER.HIDER)
      player2_move = play(player=u.PLAYER.SEEKER)
      
      pm1 = player1_move[0] * game.N + player1_move[1]
      pm2 = player2_move[0] * game.N + player2_move[1]
      
      scores.append((cur_scores[0] + payoff[pm1][pm2], cur_scores[1] - payoff[pm1][pm2]))
      
      if player1_move == player2_move:
         rounds_won.append((cur_rounds_won[0], cur_rounds_won[1] + 1))
      else:
         rounds_won.append((cur_rounds_won[0] + 1, cur_rounds_won[1]))
      
      moves.append((player1_move, player2_move))
   
   return moves, scores, rounds_won
