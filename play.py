import util as u
import numpy as np
from game import Game
from lp_solver import solve_hider_strategy, solve_seeker_strategy

def play(game: Game, player: u.PLAYER):
   """
   Args:
      game (Game): game object to play in
      player (u.PLAYER): player turn to play

   Returns:
       row, col: location of the optimal move to be played
   """
   # Play a round of the game
   return game.play_round(player)

def simulate(game: Game, rounds=100, start_turn=u.PLAYER.HIDER):
   """
   Simulate a number of rounds of the game.
   Returns:
      results: the moves made by both players in each round.
   """
   results = []
   turn = start_turn
   for _ in range(rounds):
      player1_move, player2_move = game.play_round(player=turn)
      results.append((player1_move, player2_move))
      turn = game.other(turn)
   return results
