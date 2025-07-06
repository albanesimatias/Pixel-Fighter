import pygame
from constants import *
from sprite import Sprite

def get_events_menu(selected, options):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "exit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                return (selected - 1) % len(options)
            elif event.key == pygame.K_s:
                return (selected + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                return options[selected].lower()
    return selected

def draw_menu(screen):
    try:
        image = Sprite.get_instance().get_sprite_frame(ID_Object.BACKGROUND.value, Scene.INTRO, 0)
        scaled_image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_image, (0, 0))
    except pygame.error as e:
        screen.fill((0, 0, 0))

def main_menu_screen(screen, font, options):
    selected = 0
    clock = pygame.time.Clock()

    while True:
        result = get_events_menu(selected, options)

        if isinstance(result, str):
            return result
        else:
            selected = result

        draw_menu(screen)

        for i, option in enumerate(options):
            color = Color.YELLOW.value if i == selected else Color.GRAY.value
            text = font.render(option, True, color)
            screen.blit(text, (BASE_X_MENU, BASE_Y_MENU + i * SPACING))

        pygame.display.flip()
        clock.tick(FPS)

        
