import pygame
from constants import *

def main_menu_screen(screen, font, options):
    selected = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill((10, 10, 30))

        title = font.render("Pixel-Fighter", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (150, 150, 150)
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower()
