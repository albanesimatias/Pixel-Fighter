import pygame
import threading
from enum import Enum

TITLE = "Pixel Fighter"

FONT_SIZE = 36
FONT_SIZE_TIMER = 48
FONT_FAMILY_TIMER = "arialblack"

WIDTH, HEIGHT = 800, 500
HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT = 300, 15
MAX_HP = 100
BAR_SPACING = 10

X_TIMER = 387
Y_TIMER = 0
X_SHADOW_TIMER = X_TIMER + 2
Y_SHADOW_TIMER = Y_TIMER + 2

TITLE_KO = "KO"
X_KO = 385
Y_KO = 20

BASE_X_MENU = 340
BASE_Y_MENU = 160

FPS = 60

GRAVITY = 30

### Scene Select ###
CHARACTER_LIST = ["Esteban", "Maximo", "Mariano", "Matias"]
SPACING = 60
BASE_Y = 80
BASE_X_P1 = 50
BASE_X_P2 = 620
UPDATE_SELECT = 200

PPM = 30
FIGHTING = {"is_running": True}

ROUND_DURATION = 60
time_round = [ROUND_DURATION]
timer_mtx = threading.Lock()

STATE_MENU = "menu"
STATE_SELECT = "select"
STATE_PLAYING = "playing"
STATE_OPTIONS = "options"
STATE_EXIT = "exit"

MENU_OPTIONS = ["PLAY", "EXIT"]

class State(Enum):
    IDLE = 1
    MOVE = 2
    ATTACK = 3
    BLOCK = 4
    KICKED = 5
    DISTANCE_ATTACK = 6

class Sound(Enum):
    ATTACK = 1
    JUMP = 2
    BLOCKED = 3
    KICKED = 4
    LOOP = 5

class Direction(Enum):
    RIGHT = 1
    LEFT = -1

class ID_Character(Enum):
    ESTEBAN = "Esteban"
    MAXIMO = "Maximo"
    MARIANO = "Mariano"
    MATIAS = "Matias"

class Scene(Enum):
    INTRO = 0
    SELECT = 1
    FIGHT = 2
    VICTORY = 3

class ID_Object(Enum):
    BACKGROUND = "background"
    PROJECTILE = "projectile"

class ID_Scene(Enum):
    WIN = "win"
    EMPATE = "empate"

class Color(Enum):
    PINK = (255, 200, 200)
    GRAY = (100, 100, 100)
    BLUE = (150, 200, 255)
    YELLOW = (255, 255, 0)
    RED = (180, 0, 0)
    BLACK = (0, 0, 0)
    
controls = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "down": pygame.K_s,
    "attack": pygame.K_f,
    "block": pygame.K_g
}

controls2 = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "attack": pygame.K_RCTRL,
    "block": pygame.K_RSHIFT
}


PPM = 30
WIDTH_SPRITE, HEIGHT_SPRITE = 110, 120
SHOOT_COOLDDOWN = 800
ATTACK_COOLDOWN = 500
CHARACTER_WIDTH = 40
CHARACTER_HP = 100
COOLDOWN_ANIM = 100
DENSITY = 1
FRICTION = 0.2


X_TRESHOLD = 5
Y_TRESHOLD = 12  # Sirve para determinar si el proyectil debe tener velocidad vertical hacia abajo o no.
CHANCE_ATTACK = 0.6
CHANCE_BLOCK = 0.4
SLEEP_TIME = 0.4

SLEEP = 0.5

VOLUME = 0.2

SPRITES_SIZE = (188, 128)
