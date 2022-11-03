import os
from enum import Enum

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
GREEEN_KEY = (59,210,66)

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
    PURE = 'Pure'

class POSITION():

    TREASURE = {
        MOVESET.FIRE : [1400, 1500],
        MOVESET.EARTH : [2000, 3000],
        MOVESET.WATER : [1000, 1200],
        MOVESET.ULT : [1000, 2000]
    }


attr = [MOVESET.FIRE, MOVESET.WATER, MOVESET.EARTH]

