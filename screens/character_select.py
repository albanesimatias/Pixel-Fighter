import pygame
from random import randint
from constants import *
from sprite import Sprite

CHARACTER_LIST = ["Esteban", "Maximo", "Mariano", "Matias"]


def draw_character_select(screen, font, selected_p1, selected_p2, confirm_p1, confirm_p2):
    try:
        image = Sprite.get_instance().get_sprite_frame(ID_Object.BACKGROUND.value, Scene.SELECT, 0)
        scaled_image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_image, (0, 0))
    except pygame.error as e:
        screen.fill((0, 0, 0))

    for i, name in enumerate(CHARACTER_LIST):
        color_p1 = (255, 200, 200) if i == selected_p1 else (100, 100, 100)
        color_p2 = (150, 200, 255) if i == selected_p2 else (60, 60, 60)

        name_p1 = font.render(name, True, color_p1)
        name_p2 = font.render(name, True, color_p2)

        screen.blit(name_p1, (screen.get_width() // 7 - name_p1.get_width() // 2, BASE_Y + i * SPACING))
        screen.blit(name_p2, (5 * screen.get_width() // 6 - name_p2.get_width() // 2, BASE_Y + i * SPACING))

    if confirm_p1:
        locked = font.render("✓", True, (0, 255, 0))
        screen.blit(locked, (screen.get_width() // 7 + 80, BASE_Y + selected_p1 * SPACING))
    if confirm_p2:
        locked = font.render("✓", True, (0, 255, 0))
        screen.blit(locked, (5 * screen.get_width() // 6 + 80, BASE_Y + selected_p2 * SPACING))


def character_selection_screen(screen, font):
    selected_p1 = 0
    confirm_p1 = False
    confirm_p2 = True
    clock = pygame.time.Clock()

    bot_select = randint(0, len(CHARACTER_LIST) - 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if not confirm_p1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        selected_p1 = (selected_p1 - 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_s:
                        selected_p1 = (selected_p1 + 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_RETURN:
                        confirm_p1 = True

        draw_character_select(screen, font, selected_p1, bot_select, confirm_p1, confirm_p2)
        pygame.display.flip()
        clock.tick(60)

        if confirm_p1 and confirm_p2:
            break

    return CHARACTER_LIST[selected_p1], CHARACTER_LIST[bot_select]
