import numpy as np
from scipy.optimize import linprog

def solve_hider_strategy(payoff_matrix):
   # Solve for the optimal mixed strategy for the hider (maximize minimum gain)
   num_strategies = payoff_matrix.shape[0]

   c = [-1] * num_strategies  # Objective: maximize sum (converted to minimize -sum)
   A_ub = -payoff_matrix.T    # Inequality constraints
   b_ub = [-1] * payoff_matrix.shape[1]

   A_eq = [[1] * num_strategies]  # Sum of probabilities must equal 1
   b_eq = [1]

   bounds = [(0, 1)] * num_strategies  # Probabilities between 0 and 1

   result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='simplex')
   if result.success:
      return result.x  # Return the optimal strategy (probabilities)
   else:
      raise ValueError("Linear program failed to solve.")

def solve_seeker_strategy(payoff_matrix):
   # Solve for seeker strategy by negating the payoff matrix (zero-sum game dual)
   return solve_hider_strategy(-payoff_matrix)