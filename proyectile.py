import pygame
from enum import Enum
import math


class Direction(Enum):
    RIGHT = 1
    LEFT = -1


class Projectile:
    def __init__(self, world, x, y, direction, sprite, speed=15):
        self.sprite = sprite
        self.alive = True
        self.x = x
        self.direction = direction
        self.body = world.CreateDynamicBody(
            position=(x, y),
            bullet=True,  # más precisión para colisiones rápidas
            fixedRotation=False
        )
        self.body.angularVelocity = 5 * direction.value  # velocidad angular para rotación
        self.shape = self.body.CreateCircleFixture(radius=0.2, density=1, friction=0, restitution=0)
        self.body.linearVelocity = (speed * direction.value, 0)
        self.body.gravityScale = 0

    def update(self, screen_width_px=800, margin_px=50):
        if not self.body:
            self.alive = False
            return
        x_px = self.body.position.x * 30  # PPM = 30
        velocity_x = self.body.linearVelocity.x
        if x_px < margin_px or x_px > (screen_width_px - margin_px) or abs(velocity_x) < 2:
            self.alive = False

    def draw(self, screen, ppm=30):
        if not self.body:
            return

        x = int(self.body.position.x * ppm)
        y = int(self.body.position.y * ppm)

        # Rotamos el sprite según el ángulo del cuerpo (en radianes)

        angle_degrees = -math.degrees(self.body.angle)
        rotated_image = pygame.transform.rotate(self.sprite, angle_degrees)

        # Corregimos la posición para centrar la imagen
        rect = rotated_image.get_rect(center=(x, y))

        screen.blit(rotated_image, rect)

    def destroy(self):
        self.marked_for_removal = True
