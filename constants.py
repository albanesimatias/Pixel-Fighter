import pygame
import threading
from enum import Enum

WIDTH, HEIGHT = 800, 500
HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT = 200, 15
MAX_HP = 100
BAR_SPACING = 10
Y_KO = 30
RED_HEALTH = (180, 0, 0)
YELLOW_HEALTH = (255, 215, 0)
FPS = 60
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

SPACING = 60
BASE_Y = 80


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
