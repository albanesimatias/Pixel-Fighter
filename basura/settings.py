import pygame

TIME_OPTIONS = [30, 60, 90, 120]

def draw_settings_menu(screen, font, selected_index, current_time_index):
    screen.fill((0, 0, 0))

    title = font.render("SETTINGS", True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

    option_label = font.render("ROUND TIME:", True, (255, 255, 255))
    screen.blit(option_label, (screen.get_width() // 2 - option_label.get_width() // 2, 160))

    for i, value in enumerate(TIME_OPTIONS):
        color = (255, 255, 0) if i == selected_index else (180, 180, 180)
        time_text = font.render(f"{value} SECONDS", True, color)
        screen.blit(time_text, (screen.get_width() // 2 - time_text.get_width() // 2, 220 + i * 50))

    footer = font.render("Press ENTER to confirm — ESC to return", True, (100, 100, 100))
    screen.blit(footer, (screen.get_width() // 2 - footer.get_width() // 2, screen.get_height() - 40))
