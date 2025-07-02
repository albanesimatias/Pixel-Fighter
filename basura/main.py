import pygame
import Box2D
from screens.menu import draw_main_menu
from screens.character_select import draw_character_select, CHARACTER_LIST
from screens.settings import draw_settings_menu, TIME_OPTIONS
from screens.victory_screen import victory_screen
from character import Character
from background import Background
from timer import draw_timer  
from constants import *

pygame.init()

# Pantalla
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de pelea")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 36)

# Estados
STATE_MENU = "menu"
STATE_SELECT = "select"
STATE_SETTINGS = "settings"
STATE_PLAYING = "playing"
STATE_VICTORY = "victory"

game_state = STATE_MENU
running = True

# Menú
menu_options = ["PLAY", "SETTINGS", "EXIT"]
menu_index = 0

# Selección
selected_p1 = 0
selected_p2 = 1
confirm_p1 = False
confirm_p2 = False

# Configuración
settings_index = 1
settings_selection = settings_index

# Mundo físico y suelo
PPM = 30
world = Box2D.b2World(gravity=(0, 20), doSleep=True)
ground = world.CreateStaticBody(position=(WIDTH / 2 / PPM, HEIGHT / PPM))
ground.CreatePolygonFixture(box=(WIDTH / 2 / PPM, 1), density=0, friction=0.8)

# Fondo animado
background = Background()

# Controles
controls_p1 = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'attack': pygame.K_f,
    'block': pygame.K_g
}
controls_p2 = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'attack': pygame.K_KP1,
    'block': pygame.K_KP2
}

# Jugadores y combate
player1 = None
player2 = None
round_time = 0
round_start_time = 0
victory_winner = None

# ⏱️ Cronómetro y cálculo de tiempo restante
# ⏱️ Configuración del round

start_ticks = pygame.time.get_ticks()
elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
time_left = max(0, ROUND_DURATION - elapsed_seconds)
font_timer = pygame.font.SysFont("arialblack", 60)

# Barras de vida
TEXT_KO = font.render("KO", True, (200, 0, 0))
X_KO = WIDTH // 2 - TEXT_KO.get_width() // 2

X_BAR_P1 = X_KO - HEALTH_BAR_WIDTH - BAR_SPACING
X_BAR_P2 = X_KO + TEXT_KO.get_width() + BAR_SPACING
Y_BAR = Y_KO + 5

def calculate_health_width(current_hp, max_hp, bar_width):
    hp = max(current_hp, 0)
    return int((hp / max_hp) * bar_width)
   
def draw_health_bars(surface, p1_hp, p2_hp):
    prog_p1 = calculate_health_width(p1_hp, MAX_HP, HEALTH_BAR_WIDTH)
    prog_p2 = calculate_health_width(p2_hp, MAX_HP, HEALTH_BAR_WIDTH)

    pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P1, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, RED_HEALTH, (X_BAR_P2, Y_BAR, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P1 + HEALTH_BAR_WIDTH - prog_p1, Y_BAR, prog_p1, HEALTH_BAR_HEIGHT))
    pygame.draw.rect(surface, YELLOW_HEALTH, (X_BAR_P2, Y_BAR, prog_p2, HEALTH_BAR_HEIGHT))

    surface.blit(TEXT_KO, (X_KO, Y_KO))

while running:
    draw_timer(screen, font, time_left, WIDTH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if game_state == STATE_MENU:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    selected = menu_options[menu_index]
                    if selected == "PLAY":
                        game_state = STATE_SELECT
                    elif selected == "SETTINGS":
                        game_state = STATE_SETTINGS
                    elif selected == "EXIT":
                        running = False

            elif game_state == STATE_SETTINGS:
                if event.key == pygame.K_UP:
                    settings_selection = (settings_selection - 1) % len(TIME_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    settings_selection = (settings_selection + 1) % len(TIME_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    settings_index = settings_selection
                elif event.key == pygame.K_ESCAPE:
                    game_state = STATE_MENU

            elif game_state == STATE_SELECT:
                if not confirm_p1:
                    if event.key == pygame.K_w:
                        selected_p1 = (selected_p1 - 1) % len(CHARACTER_LIST)
                        if selected_p1 == selected_p2:
                            selected_p1 = (selected_p1 - 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_s:
                        selected_p1 = (selected_p1 + 1) % len(CHARACTER_LIST)
                        if selected_p1 == selected_p2:
                            selected_p1 = (selected_p1 + 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_SPACE:
                        confirm_p1 = True

                elif not confirm_p2:
                    if event.key == pygame.K_UP:
                        prev = selected_p2
                        while True:
                            selected_p2 = (selected_p2 - 1) % len(CHARACTER_LIST)
                            if selected_p2 != selected_p1 or selected_p2 == prev:
                                break
                    elif event.key == pygame.K_DOWN:
                        prev = selected_p2
                        while True:
                            selected_p2 = (selected_p2 + 1) % len(CHARACTER_LIST)
                            if selected_p2 != selected_p1 or selected_p2 == prev:
                                break
                    elif event.key == pygame.K_RETURN:
                        if selected_p2 != selected_p1:
                            confirm_p2 = True
                        else:
                            print("❌ No se puede elegir el mismo personaje dos veces.")

                else:
                    name_p1 = CHARACTER_LIST[selected_p1]
                    name_p2 = CHARACTER_LIST[selected_p2]
                    player1 = Character(world, 150, HEIGHT - 100, controls_p1, name=name_p1)
                    player2 = Character(world, 750, HEIGHT - 100, controls_p2, name=name_p2)
                    round_time = TIME_OPTIONS[settings_index]
                    round_start_time = pygame.time.get_ticks()
                    game_state = STATE_PLAYING

            elif game_state == STATE_VICTORY:
                if event.key == pygame.K_RETURN:
                    game_state = STATE_MENU
                    menu_index = 0
                    selected_p1 = 0
                    selected_p2 = 1
                    confirm_p1 = False
                    confirm_p2 = False
                    victory_winner = None

    # RENDER
    if game_state == STATE_MENU:
        draw_main_menu(screen, font, menu_index, menu_options)

    elif game_state == STATE_SETTINGS:
        draw_settings_menu(screen, font, settings_selection, settings_index)

    elif game_state == STATE_SELECT:
        draw_character_select(screen, font, selected_p1, selected_p2, confirm_p1, confirm_p2)

    elif game_state == STATE_PLAYING:
        background.update()
        background.draw(screen)

        keys = pygame.key.get_pressed()
        player1.event_handler(keys)
        player2.event_handler(keys)

        player1.update()
        player2.update()

        player1.update_character_direction(player2)
        player2.update_character_direction(player1)

        player1.hit_check(player2)
        player2.hit_check(player1)
        player1.projectile_hit_check(player2)
        player2.projectile_hit_check(player1)

        world.Step(1.0 / 60.0, 6, 2)

        player1.draw(screen)
        player2.draw(screen)
        draw_health_bars(screen, player1.hp, player2.hp)

        elapsed = (pygame.time.get_ticks() - round_start_time) // 1000
        remaining = max(0, round_time - elapsed)
        time_text = font.render(f"TIME: {remaining}", True, (255, 255, 255))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 20))

        if remaining <= 0:
            victory_winner = player1.name
            game_state = STATE_VICTORY

    elif game_state == STATE_VICTORY:
        victory_screen(screen, font, WIDTH, HEIGHT, victory_winner or "Empate")
        game_state == STATE_MENU
        pygame.quit()

    pygame.display.flip()

