import pygame
import time
import random
from constants import *

pygame.init()

events = [
    pygame.K_LEFT,
    pygame.K_RCTRL,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_DOWN,
    pygame.K_RSHIFT
]

key_words = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_RCTRL: False,
    pygame.K_RSHIFT: False
}


def IA_PLAYER():
    while FIGHTING['is_running']:
        key_word = random.choice(events)
        key_words[key_word] = True
        key_word2 = random.choice(events)
        key_words[key_word2] = True
        time.sleep(1)
        key_words[key_word] = False
        key_words[key_word2] = False
        time.sleep(SLEEP)
