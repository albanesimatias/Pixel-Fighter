import pygame
from screens.menu import draw_main_menu
from screens.character_select import draw_character_select, CHARACTER_LIST
from character import Character
from constants import *
from Box2D import b2World


def run_main_menu(screen, font, clock, controls_p1, controls_p2):
    menu_options = ["JUGAR", "SALIR"]
    menu_index = 0
    game_state = "menu"

    selected_p1, selected_p2 = 0, 1
    confirm_p1 = False
    confirm_p2 = False

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None  # Cierra el juego

            elif event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    if event.key == pygame.K_UP:
                        menu_index = (menu_index - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        menu_index = (menu_index + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        selected = menu_options[menu_index]
                        if selected == "JUGAR":
                            game_state = "select"
                        elif selected == "SALIR":
                            return None, None

                elif game_state == "select":
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

        # Dibujar pantalla según estado
        if game_state == "menu":
            draw_main_menu(screen, font, menu_index, menu_options)
        elif game_state == "select":
            draw_character_select(screen, font, selected_p1, selected_p2, confirm_p1, confirm_p2)

        pygame.display.flip()

        # Si ambos confirmaron, devolver personajes listos para pelear
        if confirm_p1 and confirm_p2:
            world = b2World(gravity=(0, 30), doSleep=True)
            player1 = Character(world, 150, HEIGHT - 110, controls_p1, name=CHARACTER_LIST[selected_p1])
            player2 = Character(world, WIDTH - 150, HEIGHT - 110, controls_p2, name=CHARACTER_LIST[selected_p2])
            return player1, player2