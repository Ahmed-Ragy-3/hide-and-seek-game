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

      status (int): An integer representing the exit status of the algorithm.

         ``0`` : Optimization terminated successfully.

         ``1`` : Iteration limit reached.

         ``2`` : Problem appears to be infeasible.

         ``3`` : Problem appears to be unbounded.

         ``4`` : Numerical difficulties encountered.

        message (str): A string descriptor of the exit status of the algorithm.
"""

"""
   Sample Payoff Matrix:

      S1 S2 S3 S4
   H1 -1  1  1  1    x₁
   H2  2 -1  2  2    x₂
   H3  1  1 -3  1    x₃
   H4  2  2  2 -1    x₄
       y₁ y₂ y₃ y₄
   
   max z = v:
      -1 x₁ + 2x₂ +  x₃ + 2x₄ >= v
       1 x₁ -  x₂ +  x₃ + 2x₄ >= v
       1 x₁ + 2x₂ - 3x₃ + 2x₄ >= v
       1 x₁ + 2x₂ +  x₃ -  x₄ >= v
   
               ↓
               ↓ dual
               ↓

   min z = w:
      -1 y₁ + 1y₂ + 1y₃ + 1y₄ <= w
       2 y₁ - 1y₂ + 2y₃ + 2y₄ <= w
       1 y₁ + 1y₂ - 3y₃ + 1y₄ <= w
       2 y₁ + 2y₂ + 2y₃ - 1y₄ <= w

      -1 y₁ + 1y₂ + 1y₃ + 1y₄ - w <= 0
       2 y₁ - 1y₂ + 2y₃ + 2y₄ - w <= 0
       1 y₁ + 1y₂ - 3y₃ + 1y₄ - w <= 0
       2 y₁ + 2y₂ + 2y₃ - 1y₄ - w <= 0
       
                  ↓
                  ↓ eqn's * -1
                  ↓
 
      z = 0 y₁ + 0 y₂ + 0 y₃ + 0 y₄ + 1 w
         y₁ -  y₂ -  y₃ -  y₄ - w <= 0
      -2 y₁ +  y₂ - 2y₃ - 2y₄ - w <= 0
       - y₁ -  y₂ + 3y₃ -  y₄ - w <= 0
      -2 y₁ - 2y₂ - 2y₃ +  y₄ - w <= 0

                  ↓
                  ↓
                  ↓

      z - 0 y₁ - 0 y₂ - 0 y₃ - 0 y₄ - 1 w = 0
         y₁ -  y₂ -  y₃ -  y₄ + w <= 0
      -2 y₁ +  y₂ - 2y₃ - 2y₄ + w <= 0
       - y₁ -  y₂ + 3y₃ -  y₄ + w <= 0
      -2 y₁ - 2y₂ - 2y₃ +  y₄ + w <= 0

   max hider = min seeker
"""
# max z = v:
# min z = -v:
#    -1 x₁ + 2x₂ +  x₃ + 2x₄ >= v
#     1 x₁ -  x₂ +  x₃ + 2x₄ >= v
#     1 x₁ + 2x₂ - 3x₃ + 2x₄ >= v
#     1 x₁ + 2x₂ +  x₃ -  x₄ >= v

#    -1 x₁ + 2x₂ +  x₃ + 2x₄ + v <= 0
#     1 x₁ -  x₂ +  x₃ + 2x₄ + v <= 0
#     1 x₁ + 2x₂ - 3x₃ + 2x₄ + v <= 0
#     1 x₁ + 2x₂ +  x₃ -  x₄ + v <= 0

# METHOD = 'simplex'
METHOD = 'highs'

def solve(contraints: np.ndarray, primal=True) -> np.ndarray:
   print("Primal" if primal else "Dual")
   # get probabilities x₁, x₂, ............
   # Solve for the optimal mixed strategy for the hider (maximize minimum gain)
   num_strategies = contraints.shape[0]   # number of probabilities (strategies) to play
   
   # Objective: maximize v (converted to minimize -sum)
   c = [0] * num_strategies + [-1 if primal else 1]   # last element is the variable v

   # Constraints: A_ub * x <= b_ub
   A_ub = np.hstack((contraints, (1 if primal else -1) * np.ones((num_strategies, 1))))
   b_ub = [0] * num_strategies
   print(A_ub)

   # Sum of probabilities must equal 1
   A_eq = [[1] * num_strategies + [0]]   # last element is the variable v
   probs_sum = [1]

   # Probabilities between 0 and 1  ,    v unbounded
   bounds = [(0, 1)] * num_strategies + [(None, None)] 

   result = linprog(c, A_ub=A_ub, b_ub=b_ub, 
                       A_eq=A_eq, b_eq=probs_sum, 
                       method=METHOD, bounds=bounds)
   if result.success:
      return result.x[:-1]   # Return optimal strategies (probabilities) without v
   else:
      print("Optimization failed:", result.message)
      print("Status code:", result.status)
      raise ValueError("Linear program failed to solve.")


def solve_hider_strategy(payoff_matrix: np.ndarray) -> np.ndarray:
   return solve(-payoff_matrix.T, primal=True)

def solve_seeker_strategy(payoff_matrix: np.ndarray) -> np.ndarray:
   # Solve for seeker strategy by negating the payoff matrix (zero-sum game dual)
   return solve(payoff_matrix, primal=False)