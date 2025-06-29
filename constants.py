
import pygame

HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 15
MAX_HP = 100
BAR_SPACING = 10
Y_KO = 30
RED_HEALTH = (180, 0, 0)
YELLOW_HEALTH = (255, 215, 0)
ANCHO = 800
ALTO = 500
FPS = 30
PPM = 30
FIGHTING = {"is_running": True}

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
