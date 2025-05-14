import numpy as np
from scipy.optimize import linprog

"""
   c (1D array): The coefficients of the linear objective function to be minimized.
   
   A_ub * x <= b_ub
   A_eq * x  = b_eq

   Returns
      x (1D array): The values of the decision variables that minimizes the
                    objective function while satisfying the constraints.
      
      fun (float): The optimal value of the objective function ``c @ x``.
      
      success (bool): `True` when the algorithm succeeds in finding an optimal solution.
"""

# METHOD = 'simplex'
METHOD = 'highs'

def solve_hider_strategy(payoff_matrix) -> np.ndarray:
   # get probabilities x₁, x₂, ............
   # Solve for the optimal mixed strategy for the hider (maximize minimum gain)
   num_strategies = payoff_matrix.shape[0]   # number of probabilities (strategies) to play
   print(num_strategies)
   # Objective: maximize v (converted to minimize -sum)
   c = [-1] * num_strategies

   # Constraints: A_ub * x <= v_coeffs
   A_ub = -payoff_matrix.T
   # v_coeffs = [-1] * num_strategies
   v_coeffs = [-1] * payoff_matrix.shape[1]

   # Sum of probabilities must equal 1
   A_eq = [[1] * num_strategies]
   probs_sum = [1]

   # Probabilities between 0 and 1
   bounds = [(0, 1)] * num_strategies

   result = linprog(c, A_ub=A_ub, b_ub=v_coeffs, 
                       A_eq=A_eq, b_eq=probs_sum, 
                       method=METHOD, bounds=bounds)
   if result.success:
      return result.x   # Return optimal strategies (probabilities)
   else:
      raise ValueError("Linear program failed to solve.")

def solve_seeker_strategy(payoff_matrix) -> np.ndarray:
   # Solve for seeker strategy by negating the payoff matrix (zero-sum game dual)
   return solve_hider_strategy(-payoff_matrix)