def draw_timer(surface, font, time_left, screen_width):
    """
    Dibuja el cronómetro centrado arriba con borde negro.
    """
    x = screen_width // 2
    y = 10
    text_str = f"{time_left}"

    # Render principal (amarillo)
    text = font.render(text_str, True, (255, 255, 0))

    # Borde negro (efecto sombra)
    border = 2
    for dx in [-border, border]:
        for dy in [-border, border]:
            shadow = font.render(text_str, True, (0, 0, 0))
            surface.blit(shadow, (x - text.get_width() // 2 + dx, y + dy))

    # Texto encima
    surface.blit(text, (x - text.get_width() // 2, y))