import pygame


class Background:
    def __init__(self, frames, frame_time=200):
        self.frames = frames
        print(self.frames)
        self.frame = 0
        self.frame_time = frame_time
        self.last_change = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_change > self.frame_time:
            self.frame = 0 if self.frame == 1 else 1
            self.last_change = now

    def draw(self, screem):
        screem.blit(self.frames[self.frame], (0, 0))
