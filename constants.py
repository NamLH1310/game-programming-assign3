import os
from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TARGET_FPS = 60
RESOURCES_DIR = f'{os.getcwd()}/assets'
class MOVESET(Enum):
    FIRE = 'fire'
    WATER = 'water'
    EARTH = 'earth'
    DEF = 'defend'
    ATT = 'attack'
    ULT = 'ultimate'
    BUFF = 'buff'
    DEBUFF = 'debuff'
    TRAP = 'trap'  

attr = [MOVESET.FIRE, MOVESET.WATER, MOVESET.EARTH]