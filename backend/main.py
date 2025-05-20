import util as u
from game import Game
from simulation import simulate

def main():
   # Initialize the game with parameters N and M
   M = 4  # Example value for M
   N = 4  # Example value for N
   game = Game(N, M)
   print(game)

   # Print the game object
   # game.play_optimal(u.PLAYER.HIDER)
   # game.play_optimal(u.PLAYER.SEEKER)
   moves, scores, rounds_won = simulate(game, is_optimal=True, rounds=20)
   # print("Moves:", moves)
   for m in moves:
      print(m)

   for s in scores:
      print(s)
   # print("Scores:", scores)
   for r in rounds_won:
      print(r)
   # print("Rounds Won:", rounds_won)
   
   # res = simulate(game, rounds=20)
   # print(res)

if __name__ == "__main__":
   main()