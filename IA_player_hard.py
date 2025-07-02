import pygame
import time
import random
from constants import *

pygame.init()


distance_actions = [pygame.K_DOWN,  pygame.K_LEFT]
distance_actions2 = [pygame.K_DOWN, pygame.K_RIGHT]
dodge_action = {Direction.LEFT: pygame.K_RIGHT, Direction.RIGHT: pygame.K_LEFT}

key_words = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_RCTRL: False,
    pygame.K_RSHIFT: False
}


def IA_PLAYER(jugador1, jugador2):
    while FIGHTING['is_running']:
        for key in key_words:
            key_words[key] = False

        pos1 = jugador1.body.position
        pos2 = jugador2.body.position
        dx = pos1[0] - pos2[0]
        distancia_horizontal = abs(dx)

        if distancia_horizontal > X_TRESHOLD:
            if jugador2.direction.value == Direction.LEFT.value:
                key_words[distance_actions[random.randint(0, 1)]] = True
            else:
                key_words[distance_actions2[random.randint(0, 1)]] = True
        else:
            if random.random() < CHANCE_ATTACK:
                key_words[pygame.K_RCTRL] = True
            elif random.random() < CHANCE_BLOCK:
                key_words[pygame.K_RSHIFT] = True
            else:
                key_words[dodge_action[jugador2.direction]] = True
        time.sleep(SLEEP_TIME)
