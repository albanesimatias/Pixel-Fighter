import pygame
from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody
import os
from character import Character, State  # asumimos que guardaste la clase arriba aquí
from background import Background  # asumimos que guardaste la clase arriba aquí
from victory_screen import victory_screem

pygame.init()
ANCHO, ALTO = 800, 500
font = pygame.font.SysFont(None, 36)



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

#dibujar la barra
def draw_health_bar(surface, x, y, width, height, background_color, health_color, current_width):
    """
    Draws a health bar that shrinks from right to left as health decreases.

    :param surface: Pygame surface to draw on (e.g., screen)
    :param x: X coordinate of the top-left corner
    :param y: Y coordinate of the top-left corner
    :param width: Total width of the bar
    :param height: Height of the bar
    :param background_color: Color for the empty part (e.g., red)
    :param health_color: Color for the filled part (e.g., yellow)
    :param current_width: How much of the bar is filled (based on HP)
    """
    pygame.draw.rect(surface, background_color, (x, y, width, height))
    pygame.draw.rect(surface, health_color, (x + width - current_width, y, current_width, height))

def calculate_health_width(current_hp, max_hp, bar_width):
    hp = max(current_hp, 0)
    return int((hp / max_hp) * bar_width)


sprites = {
    State.IDLE: load_sprites("assets/sprites/idle", size=(94*2, 64*2)),
    State.MOVE: load_sprites("assets/sprites/mover", size=(94*2, 64*2)),
    State.ATTACK: load_sprites("assets/sprites/atacar", size=(94*2, 64*2)),
    State.BLOCK: load_sprites("assets/sprites/bloquear", size=(94*2, 64*2)),
    State.KICKED: load_sprites("assets/sprites/daño", size=(94*2, 64*2)),
    State.DISTANCE_ATTACK: load_sprites("assets/sprites/lanzar", size=(94*2, 64*2)),
    State.PROYECTILE: load_sprites("assets/sprites/proyectile", size=(64, 64))
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

player = Character(world, 100, 100, sprites, controls,name="player")
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

    player.projectile_hit_check(player2)
    player2.projectile_hit_check(player)

    player.update_character_direction(player2)
    player2.update_character_direction(player)

    # Dibujar
    background.update()
    background.draw(screem)
    player.draw(screem)
    player2.draw(screem)


    texto_ko = font.render("KO", True, (200, 0, 0))
    x_ko = ANCHO // 2 - texto_ko.get_width() // 2
    y_ko = 30

    # Dimensiones de barras
    barra_ancho = 200
    barra_alto = 15
    max_hp = 100

    # Vida actual
    prog_p1 = calculate_health_width(player.hp, max_hp, barra_ancho)
    prog_p2 = calculate_health_width(player2.hp, max_hp, barra_ancho)

    # --- Posicionamiento ---
    espacio_entre = 10  # Separación opcional mínima

    x_barra_p1 = x_ko - barra_ancho - espacio_entre
    x_barra_p2 = x_ko + texto_ko.get_width() + espacio_entre
    y_barra = y_ko + 5  # Alineado con KO

    # --- Dibujar barras ---
    rojo = (180, 0, 0)
    amarillo = (255, 215, 0)
 
    # Jugador 1 - izquierda del KO
    draw_health_bar(screem, x_barra_p1, y_barra, barra_ancho, barra_alto, rojo, amarillo, prog_p1)
    # Jugador 2 (retroceso desde derecha)
    draw_health_bar(screem, x_barra_p2, y_barra, barra_ancho, barra_alto, rojo, amarillo, prog_p2)

    # Finalmente, dibujar el KO centrado
    screem.blit(texto_ko, (x_ko, y_ko))
    

    if player2.hp <= 0 or player.hp <= 0:
        winner = player.name if player.hp > 0 else player2.name
        print(f"El ganador es: {winner}")
        victory_screem(screem, font, ANCHO, ALTO, winner) 
        fighting = False
    pygame.display.flip()

pygame.quit()
