import pygame

def victory_screen(screen, font, ANCHO, ALTO, ganador):
    victory = True
    while victory:
        screen.fill((0, 0, 0))
        texto = font.render(f"¡{ganador.upper()} gana la pelea!", True, (255, 255, 0))
        instruccion = font.render("Presioná ESC para salir", True, (200, 200, 200))

        screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 40))
        screen.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO // 2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                victory = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                victory = False