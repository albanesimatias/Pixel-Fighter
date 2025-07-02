import pygame
import threading

from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody

from sound_manager import SoundManager
from character import Character
from background import Background
from screens.victory_screen import victory_screen
from timer import draw_timer
from constants import *
import IA_player

pygame.init()
font = pygame.font.SysFont(None, 36)

TEXT_KO = font.render("KO", True, (200, 0, 0))
FONT_KO_WIDTH = TEXT_KO.get_width()
X_KO = WIDTH // 2 - FONT_KO_WIDTH // 2
Y_KO = 20
X_BAR_P1 = X_KO - HEALTH_BAR_WIDTH - BAR_SPACING
X_BAR_P2 = X_KO + FONT_KO_WIDTH + BAR_SPACING
Y_BAR = Y_KO + 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pelea con Box2D")

clock = pygame.time.Clock()

# Crear mundo físico
world = b2World(gravity=(0, 30), doSleep=True)

# Piso ajustado
floor = world.CreateStaticBody(position=(WIDTH / 2 / PPM, (HEIGHT - 70) / PPM))
floor.CreatePolygonFixture(box=(WIDTH / 2 / PPM, 0.5), density=0, friction=0.8)

# Paredes laterales
left_wall = world.CreateStaticBody(
    position=(5 / PPM, HEIGHT / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
)

right_wall = world.CreateStaticBody(
    position=((WIDTH - 5) / PPM, HEIGHT / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
)

# Controles
controls = {
    'left': pygame.K_a, 'right': pygame.K_d,
    'up': pygame.K_w, 'down': pygame.K_s,
    'attack': pygame.K_f, 'block': pygame.K_g
}
controls2 = {
    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
    'up': pygame.K_UP, 'down': pygame.K_DOWN,
    'attack': pygame.K_KP1, 'block': pygame.K_KP2
}

# Instanciar personajes y fondo
player = Character(world, 150, HEIGHT - 110, controls, name=ID_Character.ESTEBAN.value)
player2 = Character(world, WIDTH - 150, HEIGHT - 110, controls2, name=ID_Character.MAXIMO.value)
background = Background()

# Iniciar IA (si se usa)
thread = threading.Thread(target=IA_player.IA_PLAYER)
thread.start()

# Banderas y tiempo
FIGHTING = {'is_running': True}
ROUND_DURATION = 60
start_ticks = pygame.time.get_ticks()

# Loop principal de combate
while FIGHTING['is_running']:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()


    keys = pygame.key.get_pressed()
    player.event_handler(keys)
    player2.event_handler(keys)

    world.Step(1.0 / FPS, 6, 2)

    player.update()
    player2.update()

    player.update_character_direction(player2)
    player2.update_character_direction(player)

    player.hit_check(player2)
    player2.hit_check(player)
    player.projectile_hit_check(player2)
    player2.projectile_hit_check(player)

    background.update()
    background.draw(screen)
    player.draw(screen)
    player2.draw(screen)

    # Barras de vida
    def calculate_health_width(current_hp, max_hp, bar_width):
        hp = max(current_hp, 0)
        return int((hp / max_hp) * bar_width)

    def draw_health_bars():
        prog_p1 = calculate_health_width(player.hp, MAX_HP, HEALTH_BAR_WIDTH)
        prog_p2 = calculate_health_width(player2.hp, MAX_HP, HEALTH_BAR_WIDTH)
        pygame.draw.rect(screen, RED_HEALTH, (X_BAR_P1, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(screen, RED_HEALTH, (X_BAR_P2, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(screen, YELLOW_HEALTH, (X_BAR_P1 + HEALTH_BAR_WIDTH - prog_p1, Y_BAR, prog_p1, HEALTH_BAR_HEIGHT))
        pygame.draw.rect(screen, YELLOW_HEALTH, (X_BAR_P2, Y_BAR, prog_p2, HEALTH_BAR_HEIGHT))
        #screen.blit(TEXT_KO, (X_KO, Y_KO))

    draw_health_bars()

    # Cronómetro
    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, ROUND_DURATION - elapsed)
    draw_timer(screen, font, time_left, WIDTH)

    # Verificar fin del combate
    game_over = False
    winner = None

    if player.hp <= 0 or player2.hp <= 0:
        winner = player.name if player.hp > 0 else player2.name
        game_over = True
    elif time_left <= 0:
        if player.hp > player2.hp:
            winner = player.name
        elif player2.hp > player.hp:
            winner = player2.name
        else:
            winner = "empate"
        game_over = True

    if game_over:
        print(f"El ganador es: {winner}")
        victory_screen(screen, font, WIDTH, HEIGHT, winner)
        FIGHTING['is_running'] = False

    pygame.display.flip()

thread.join()
pygame.quit()