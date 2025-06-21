import pygame
from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody
import os
from character import Character  # asumimos que guardaste la clase arriba aquí
from background import Background  # asumimos que guardaste la clase arriba aquí

pygame.init()
ANCHO, ALTO = 800, 500
screem = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pelea con Box2D")

clock = pygame.time.Clock()
FPS = 30

# Escala física
PPM = 30

# Crear world Box2D
world = b2World(gravity=(0, 30), doSleep=True)

# floor (estático)
floor = world.CreateStaticBody(position=(ANCHO / 2 / PPM, (ALTO-60) / PPM))
floor.CreatePolygonFixture(box=(ANCHO / 2 / PPM, 0.5), density=0, friction=0.8)

left_wall = world.CreateStaticBody(
    position=(0.25, ALTO / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, ALTO / 2 / PPM))
)

right_wall = world.CreateStaticBody(
    position=((ANCHO - 10) / PPM, ALTO / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, ALTO / 2 / PPM))
)

# Cargar sprites


def load_sprites(path, size=None):
    sprites = []
    for file in sorted(os.listdir(path)):
        if file.endswith(".png") or file.endswith(".jpg"):
            image = pygame.image.load(os.path.join(path, file)).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            sprites.append(image)
    return sprites


sprites = {
    'idle': load_sprites("assets/sprites/idle", size=(94*2, 64*2)),
    'move': load_sprites("assets/sprites/mover", size=(94*2, 64*2)),
    'attack': load_sprites("assets/sprites/atacar", size=(94*2, 64*2)),
    'block': load_sprites("assets/sprites/bloquear", size=(94*2, 64*2)),
    'kicked': load_sprites("assets/sprites/daño", size=(94*2, 64*2))
}

background_sprites = load_sprites("assets/sprites/fondo", size=(ANCHO, ALTO))

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

player = Character(world, 100, 100, sprites, controls)
player2 = Character(world, 300, 100, sprites, controls2, name='player2')
background = Background(background_sprites)


# Loop principal
fighting = True
while fighting:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fighting = False

    key_words = pygame.key.get_pressed()
    player.event_handler(key_words)
    player2.event_handler(key_words)

    # Avanzar física
    world.Step(1.0 / FPS, 6, 2)

    player.update()
    player2.update()
    player.hit_check(player2)
    player2.hit_check(player)
    player.update_character_direction(player2)
    player2.update_character_direction(player)

    # Dibujar
    background.update()
    background.draw(screem)
    player.draw(screem)
    player2.draw(screem)

    if player2.hp <= 0 or player.hp <= 0:
        winner = player.name if player.hp > 0 else player2.name
        print(f"El ganador es: {winner}")
        fighting = False
    pygame.display.flip()

pygame.quit()
