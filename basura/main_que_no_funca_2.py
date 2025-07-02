import pygame
from screens.menu import draw_main_menu
from screens.character_select import draw_character_select, CHARACTER_LIST
from run import run_combat
from character import Character
from constants import *

pygame.init()

WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pantalla Principal")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 36)

# Estados
STATE_MENU = "menu"
STATE_SELECT = "select"
STATE_EXIT = "exit"

game_state = STATE_MENU
menu_options = ["PLAY", "EXIT"]
menu_index = 0

# Selección
selected_p1 = 0
selected_p2 = 1
confirm_p1 = False
confirm_p2 = False

# Controles (pueden extraerse si querés tener más modularidad)
controls_p1 = {
    'left': pygame.K_a, 'right': pygame.K_d,
    'up': pygame.K_w, 'down': pygame.K_s,
    'attack': pygame.K_f, 'block': pygame.K_g
}
controls_p2 = {
    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
    'up': pygame.K_UP, 'down': pygame.K_DOWN,
    'attack': pygame.K_KP1, 'block': pygame.K_KP2
}

while  game_state!=STATE_EXIT:
    print("a")
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game_state = STATE_EXIT

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
                    elif selected == "EXIT":
                        game_state = STATE_EXIT

            elif game_state == STATE_SELECT:
                if not confirm_p1:
                    if event.key == pygame.K_w:
                        selected_p1 = (selected_p1 - 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_s:
                        selected_p1 = (selected_p1 + 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_SPACE:
                        confirm_p1 = True

                elif not confirm_p2:
                    if event.key == pygame.K_UP:
                        selected_p2 = (selected_p2 - 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_DOWN:
                        selected_p2 = (selected_p2 + 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_RETURN:
                        if selected_p2 != selected_p1:
                            confirm_p2 = True
                        else:
                            print("❌ Personaje duplicado")

                else:
                    # Crear personajes y correr el loop de pelea
                    from Box2D import b2World
                    world = b2World(gravity=(0, 30), doSleep=True)

                    player1 = Character(world, 150, HEIGHT - 100, controls_p1, name=CHARACTER_LIST[selected_p1])
                    player2 = Character(world, 750, HEIGHT - 100, controls_p2, name=CHARACTER_LIST[selected_p2])
                    FIGHTING = {'is_running': True}

                    #run_combat([player1, player2], FIGHTING)
                    # Reiniciar selección luego de la pelea
                    selected_p1, selected_p2 = 0, 1
                    confirm_p1, confirm_p2 = False, False
                    game_state = STATE_MENU
                    FIGHTING['is_running'] = False
                    print("pase por aca")

    # Dibujar pantallas
    if game_state == STATE_MENU:
        screen.fill((20, 20, 20))
        draw_main_menu(screen, font, menu_index, menu_options)

    elif game_state == STATE_SELECT:
        screen.fill((20, 20, 60))
        draw_character_select(screen, font, selected_p1, selected_p2, confirm_p1, confirm_p2)

    pygame.display.flip()

pygame.quit()