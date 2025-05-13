from enum import Enum

class PLACETYPE(Enum):
   """
   - Hard: the seeker gets higher points upon winning (hider gets lower)
   - Neutral: both hider and seeker get the same points upon winning.
   - Easy: the seeker gets lower points upon winning (hider gets higher)
   """
   HARD = 'hard'
   NEUTRAL = 'neutral'
   EASY = 'easy'

   def __str__(self):
      return self.value
class PLAYER(Enum):
   HIDER = 'hider'
   SEEKER = 'seeker'

   def __str__(self):
      return self.value

class MODE(Enum):
   INTERACTIVE = 'interactive'
   SIMULATION = 'simulation'
   
   def __str__(self):
      return self.value

class linear_iterator:
   def __init__(self, matrix, get_indices=False):
      self.matrix = matrix
      self.M = len(matrix)
      self.N = len(matrix[0]) if self.M > 0 else 0
      self.total = self.M * self.N
      self.index = 0
      self.get_indices = get_indices

   def __iter__(self):
      return self

   def __next__(self):
      if self.index >= self.total:
         raise StopIteration

      row = self.index // self.N
      col = self.index % self.N
      value = self.matrix[row][col]
      self.index += 1

      if self.get_indices:
         return row, col, value
      else:
         return value

subscripts = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']

def sub(number) -> str:
   sub = ""
   while number != 0:
      sub += subscripts[number % 10]
      number //= 10
   
   return sub[::-1]