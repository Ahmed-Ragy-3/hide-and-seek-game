
# gui.py
import tkinter as tk
import numpy as np
from tkinter import messagebox
from game import Game
from lp_solver import solve_hider_strategy, solve_seeker_strategy

class HideAndSeekApp:
    def __init__(self, root):
      self.root = root
      self.root.title("Hide & Seek Game")

      self.N = 4  # Number of places
      self.game = Game(self.N)

      self.role = tk.StringVar(value='hider')  # Default role
      self.rounds_played = 0
      self.player_score = 0
      self.computer_score = 0

      self.build_interface()

    def build_interface(self):
      # Build GUI elements: role selector, place buttons, status label, reset button
      tk.Label(self.root, text="Choose Role:").pack()
      tk.Radiobutton(self.root, text="Hider", variable=self.role, value='hider').pack()
      tk.Radiobutton(self.root, text="Seeker", variable=self.role, value='seeker').pack()

      self.buttons = []
      for i in range(self.N):
         # Create button for each place
         btn = tk.Button(self.root, text=f"Place {i + 1}", command=lambda i=i: self.play_round(i))
         btn.pack(pady=2)
         self.buttons.append(btn)

      self.status = tk.Label(self.root, text="")
      self.status.pack()

      tk.Button(self.root, text="Reset", command=self.reset_game).pack()

    def play_round(self, move):
      # Called when user clicks a place button
      matrix = self.game.get_matrix()

      if self.role.get() == 'hider':
         strategy = solve_seeker_strategy(matrix)
         comp_move = np.random.choice(range(self.N), p=strategy)
      else:
         strategy = solve_hider_strategy(matrix)
         comp_move = np.random.choice(range(self.N), p=strategy)

      ps, cs = self.game.play_round(self.role.get(), move, comp_move)

      # Update scores and round count
      self.rounds_played += 1
      self.player_score += ps
      self.computer_score += cs

      self.status.config(text=f"Round {self.rounds_played}: You {ps}, Computer {cs}. Total You: {self.player_score}, Computer: {self.computer_score}")

    def reset_game(self):
      # Reset game state and GUI display
      self.game.reset_world()
      self.rounds_played = 0
      self.player_score = 0
      self.computer_score = 0
      self.status.config(text="Game reset.")


def start_gui():
   root = tk.Tk()
   app = HideAndSeekApp(root)
   root.mainloop()

if __name__ == "__main__":
   start_gui()