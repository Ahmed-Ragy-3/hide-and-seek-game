import util as u
from game import Game
from play import simulate, play

def main():
   # Initialize the game with parameters N and M
   M = 1  # Example value for M
   N = 4  # Example value for N
   game = Game(N, M)

   # Print the game object
   play(game, u.PLAYER.HIDER)
   play(game, u.PLAYER.SEEKER)
   print(game)

   res = simulate(game, rounds=20)
   print(res)

if __name__ == "__main__":
   main()