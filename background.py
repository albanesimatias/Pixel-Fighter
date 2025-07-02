import pygame
from sprite import Sprite
from constants import ID_Object, Scene


class Background:
    def __init__(self, frame_time=200):
        self.frame = 0
        self.frame_time = frame_time
        self.last_change = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_change > self.frame_time:
            self.frame = 1 - self.frame
            self.last_change = now

    def draw(self, screen):
        raw_image = Sprite.get_instance().get_sprite_frame(ID_Object.BACKGROUND.value, Scene.FIGHT, self.frame)
        scaled_image = pygame.transform.scale(raw_image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_image, (0, 0))
