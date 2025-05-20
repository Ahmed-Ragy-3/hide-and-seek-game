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

subscripts = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']

type_scores = {
   # (hider score, seeker score)
   # (incase hider is not found, incase hider is found)
   PLACETYPE.HARD:    (1, 2),
   PLACETYPE.NEUTRAL: (1, 1),
   PLACETYPE.EASY:    (2, 1)
}

def sub(number) -> str:
   sub = ""
   while number != 0:
      sub += subscripts[number % 10]
      number //= 10
   
   return sub[::-1]