
import pygame
from sprite import Sprite
from constants import ID_Scene

def victory_screen(screen, font, ANCHO, ALTO, winner_name):
    victory = True

    # Ruta a la imagen de victoria según el nombre del ganador
    try:
        win_image = Sprite.get_instance().get_sprite_frame(ID_Scene.WIN.value, winner_name, 0)
    except pygame.error as e:
        print(f"[ERROR] No se pudo cargar la imagen de victoria: {e}")
        win_image = None  # Podés reemplazar con un placeholder si querés

    while victory:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                victory = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                victory = False
                return


        screen.fill((0, 0, 0))

        # Imagen de victoria centrada
        if win_image:
            x_img = ANCHO // 2 - win_image.get_width() // 2
            y_img = ALTO // 2 - win_image.get_height() // 2 - 40
            screen.blit(win_image, (x_img, y_img))

        # Texto ganador
        if winner_name.lower() != "empate":
            text = font.render(f"{winner_name.upper()} GANA LA PELEA!", True, (255, 255, 0))
        else:
            text = font.render("¡EMPATE!", True, (255, 255, 255))

        screen.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 2 + 20))

        # Instrucción para salir
        instruction = font.render("Presioná ESC para salir", True, (180, 180, 180))
        screen.blit(instruction, (ANCHO // 2 - instruction.get_width() // 2, ALTO // 2 + 60))

        pygame.display.flip()
