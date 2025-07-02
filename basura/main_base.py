from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody
from sound_manager import SoundManager

from character import Character  # asumimos que guardaste la clase arriba aquí
from background import Background  # asumimos que guardaste la clase arriba aquí
from screens.victory_screen import victory_screen
from constants import *
import IA_player
import threading


pygame.init()
font = pygame.font.SysFont(None, 36)

TEXT_KO = pygame.font.SysFont(None, 36).render("KO", True, (200, 0, 0))
X_KO = WIDTH // 2 - TEXT_KO.get_width() // 2

X_BAR_P1 = X_KO - HEALTH_BAR_WIDTH - BAR_SPACING
X_BAR_P2 = X_KO + TEXT_KO.get_width() + BAR_SPACING
Y_BAR = Y_KO + 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pelea con Box2D")


clock = pygame.time.Clock()

# Crear world Box2D
world = b2World(gravity=(0, 30), doSleep=True)

# floor (estático)
floor = world.CreateStaticBody(position=(WIDTH / 2 / PPM, (HEIGHT-60) / PPM))
floor.CreatePolygonFixture(box=(WIDTH / 2 / PPM, 0.5), density=0, friction=0.8)

left_wall = world.CreateStaticBody(
    position=(0.25, HEIGHT / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
)

right_wall = world.CreateStaticBody(
    position=((WIDTH - 10) / PPM, HEIGHT / 2 / PPM),
    shapes=b2PolygonShape(box=(0.5, HEIGHT / 2 / PPM))
)


def calculate_health_width(current_hp, max_hp, bar_width):
    hp = max(current_hp, 0)
    return int((hp / max_hp) * bar_width)


def draw_health_bars(surface, p1_healt, p2_healt):
    # Vida actual
    prog_p1 = calculate_health_width(p1_healt, MAX_HP, HEALTH_BAR_WIDTH)
    prog_p2 = calculate_health_width(p2_healt, MAX_HP, HEALTH_BAR_WIDTH)

    pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P1, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P2, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P1 + HEALTH_BAR_WIDTH - prog_p1, Y_BAR, prog_p1, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P2, Y_BAR, prog_p2, HEALTH_BAR_HEIGHT))

    screen.blit(TEXT_KO, (X_KO, Y_KO))


player = Character(world, 100, 300, controls, name=ID_Character.ESTEBAN.value)
player2 = Character(world, WIDTH * 0.8, 300, controls2, name=ID_Character.MAXIMO.value)
background = Background()

thread = threading.Thread(target=IA_player.IA_PLAYER)
thread.start()

while FIGHTING['is_running']:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            FIGHTING['is_running'] = False

    key_words = pygame.key.get_pressed()
    key_words2 = key_words  # IA_player.key_words  # if SINGLE_PLAYER else key_words

    player.event_handler(key_words)
    player2.event_handler(key_words2)

    # Avanzar física
    world.Step(1.0 / FPS, 6, 2)

    # Actualizar personajes
    player.update()
    player2.update()

    # Comprobar colisiones
    player.hit_check(player2)
    player2.hit_check(player)
    player.projectile_hit_check(player2)
    player2.projectile_hit_check(player)

    # Actualizar dirección de los personajes para que miren al oponente
    player.update_character_direction(player2)
    player2.update_character_direction(player)

    # Dibujar
    background.update()
    background.draw(screen)
    player.draw(screen)
    player2.draw(screen)
    draw_health_bars(screen, player.hp, player2.hp)

    if player2.hp <= 0 or player.hp <= 0:
        winner = player.name if player.hp > 0 else player2.name
        print(f"El ganador es: {winner}")
        victory_screen(screen, font, WIDTH, HEIGHT, winner)
        FIGHTING['is_running'] = False

    pygame.display.flip()

thread.join()
pygame.quit()