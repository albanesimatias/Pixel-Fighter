import pygame
from constants import Direction
import math


class Projectile:
    def __init__(self, world, x, y, direction, sprite, speed=15):
        self.world = world
        self.sprite = sprite
        self.alive = True
        self.x = x
        self.direction = direction
        self.body = world.CreateDynamicBody(
            position=(x, y),
            bullet=True,
            fixedRotation=False
        )
        self.body.angularVelocity = 5 * direction.value
        self.shape = self.body.CreateCircleFixture(radius=0.2, density=1, friction=0, restitution=0)
        self.body.linearVelocity = (speed * direction.value, 0)
        self.body.gravityScale = 0

    def update(self, screen_width_px=800, margin_px=50):
        if not self.body:
            self.alive = False
            self.world.DestroyBody(self.body)
            return
        x_px = self.body.position.x * 30
        velocity_x = self.body.linearVelocity.x
        velocity_y = self.body.linearVelocity.y
        if x_px < margin_px or x_px > (screen_width_px - margin_px) or abs(velocity_x) < 2 or velocity_y != 0:
            self.alive = False
            self.world.DestroyBody(self.body)

    def draw(self, screen, ppm=30):
        if not self.body:
            return

        x = int(self.body.position.x * ppm)
        y = int(self.body.position.y * ppm)

        angle_degrees = -math.degrees(self.body.angle)
        rotated_image = pygame.transform.rotate(self.sprite, angle_degrees)

        rect = rotated_image.get_rect(center=(x, y))

        screen.blit(rotated_image, rect)

    def destroy(self):
        self.marked_for_removal = True
