import pygame
from random import randint
from constants import *
from sprite import Sprite

def get_events_character_select(selected_p1, confirm_p1):
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
    return selected_p1, confirm_p1

def update_character_select(frame):
    return 1 - frame

def draw_character_select(screen, image, frame, font, selected_p1, selected_p2):
    image = pygame.transform.scale(image[frame], (screen.get_width(), screen.get_height()))
    screen.blit(image, (0, 0))
   
    for i, name in enumerate(CHARACTER_LIST):
        color_p1 = Color.PINK.value if i == selected_p1 else Color.GRAY.value
        color_p2 = Color.BLUE.value if i == selected_p2 else Color.GRAY.value

        name_p1 = font.render(name, True, color_p1)
        name_p2 = font.render(name, True, color_p2)

        screen.blit(name_p1, (BASE_X_P1, BASE_Y + i * SPACING))
        screen.blit(name_p2, (BASE_X_P2, BASE_Y + i * SPACING))

def character_selection_screen(screen, font):
    frame = 0
    last_update = 0
    selected_p1 = 0
    confirm_p1 = False
    confirm_p2 = True
    clock = pygame.time.Clock()

    bot_select = randint(0, len(CHARACTER_LIST) - 1)

    image = Sprite.get_instance().get_sprite(ID_Object.BACKGROUND.value, Scene.SELECT)

    while True:
        selected_p1, confirm_p1 = get_events_character_select(selected_p1, confirm_p1)
        now = pygame.time.get_ticks()
        if now - last_update >= UPDATE_SELECT:
            last_update = now
            frame = update_character_select(frame)
        draw_character_select(screen, image, frame, font, selected_p1, bot_select)
        pygame.display.flip()
        clock.tick(FPS)

        if confirm_p1 and confirm_p2:
            break

    return CHARACTER_LIST[selected_p1], CHARACTER_LIST[bot_select]
