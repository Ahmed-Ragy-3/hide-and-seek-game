from game import Game
from simulation import run_simulation

def main():
   # Initialize the game with parameters N and M
   M = 2  # Example value for M
   N = 3  # Example value for N
   # game = Game(N, M)
   run_simulation(N, 'hider', rounds=20)

   # Print the game object
   # print(game)

if __name__ == "__main__":
   main()