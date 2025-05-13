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

class PLAYER(Enum):
   HIDER = 'hider'
   SEEKER = 'seeker'

class MODE(Enum):
   INTERACTIVE = 'interactive'
   SIMULATION = 'simulation'

class linear_iterator:
   def __init__(self, matrix, get_indices=False):
      self.matrix = matrix
      self.rows = len(matrix)
      self.cols = len(matrix[0]) if self.rows > 0 else 0
      self.total = self.rows * self.cols
      self.index = 0
      self.get_indices = get_indices

   def __iter__(self):
      return self

   def __next__(self):
      if self.index >= self.total:
         raise StopIteration

      row = self.index // self.cols
      col = self.index % self.cols
      value = self.matrix[row][col]
      self.index += 1

      if self.get_indices:
         return row, col, value
      else:
         return value


PLACE_TYPES = ['hard', 'neutral', 'easy']