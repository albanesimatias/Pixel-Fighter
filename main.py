from Box2D.b2 import world as b2World
from Box2D import b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody
from sound_manager import SoundManager

from character import Character  # asumimos que guardaste la clase arriba aquí
from background import Background  # asumimos que guardaste la clase arriba aquí
from victory_screen import victory_screen
from constants import *
import IA_player
import threading


pygame.init()

font = pygame.font.SysFont(None, 36)

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

# dibujar la barra


def draw_health_bar(surface, x, y, width, height, background_color, health_color, current_width, reverse=False):
    pygame.draw.rect(surface, background_color, (x, y, width, height))
    if reverse:
        pygame.draw.rect(surface, health_color, (x + width - current_width, y, current_width, height))
    else:
        pygame.draw.rect(surface, health_color, (x, y, current_width, height))


def calculate_health_width(current_hp, max_hp, bar_width):
    hp = max(current_hp, 0)
    return int((hp / max_hp) * bar_width)


player = Character(world, 100, 300, controls, name=ID_Character.ESTEBAN.value)
player2 = Character(world, WIDTH * 0.8, 300, controls2, name=ID_Character.MAXIMO.value)
background = Background()

# Loop principal
thread = threading.Thread(target=IA_player.IA_PLAYER)  # Iniciar IA en un hilo
thread.start()

while FIGHTING['is_running']:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            FIGHTING['is_running'] = False

    key_words = pygame.key.get_pressed()
    key_words2 = IA_player.key_words  # if SINGLE_PLAYER else key_words
    player.event_handler(key_words)
    player2.event_handler(key_words2)

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
    background.draw(screen)
    player.draw(screen)
    player2.draw(screen)

    text_ko = font.render("KO", True, (200, 0, 0))
    x_ko = WIDTH // 2 - text_ko.get_width() // 2

    # Vida actual
    prog_p1 = calculate_health_width(player.hp, MAX_HP, HEALTH_BAR_WIDTH)
    prog_p2 = calculate_health_width(player2.hp, MAX_HP, HEALTH_BAR_WIDTH)

    # --- Posicionamiento ---

    x_bar_p1 = x_ko - HEALTH_BAR_WIDTH - BAR_SPACING
    x_bar_p2 = x_ko + text_ko.get_width() + BAR_SPACING
    y_bar = Y_KO + 5  # Alineado con KO

    # Jugador 1 - izquierda del KO
    draw_health_bar(screen, x_bar_p1, y_bar, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT, RED_HEALTH, YELLOW_HEALTH, prog_p1)
    # Jugador 2 (retroceso desde derecha)
    draw_health_bar(screen, x_bar_p2, y_bar, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT, RED_HEALTH, YELLOW_HEALTH, prog_p2, reverse=True)

    # Finalmente, dibujar el KO centrado
    screen.blit(text_ko, (x_ko, Y_KO))

    if player2.hp <= 0 or player.hp <= 0:
        winner = player.name if player.hp > 0 else player2.name
        print(f"El ganador es: {winner}")
        victory_screen(screen, font, WIDTH, HEIGHT, winner)
        FIGHTING['is_running'] = False

    pygame.display.flip()

thread.join()  # Esperar a que el hilo de IA termine
pygame.quit()
