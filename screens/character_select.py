import pygame

CHARACTER_LIST = ["Esteban", "Maximo", "Dario", "Mariano","Matias"]  # Podés expandir esta lista

def draw_character_select(screen, font, selected_p1, selected_p2, confirm_p1, confirm_p2):
    screen.fill((15, 15, 30))  # Fondo oscuro

    title = font.render("Characters", True, (255, 255, 255))
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 40))

    spacing = 60
    base_y = 150

    for i, name in enumerate(CHARACTER_LIST):
        color_p1 = (255, 200, 200) if i == selected_p1 else (100, 100, 100)
        color_p2 = (150, 200, 255) if i == selected_p2 else (60, 60, 60)

        name_p1 = font.render(name, True, color_p1)
        name_p2 = font.render(name, True, color_p2)

        screen.blit(name_p1, (screen.get_width() // 4 - name_p1.get_width() // 2, base_y + i * spacing))
        screen.blit(name_p2, (3 * screen.get_width() // 4 - name_p2.get_width() // 2, base_y + i * spacing))

    # Indicadores de confirmación
    if confirm_p1:
        locked = font.render("✓", True, (0, 255, 0))
        screen.blit(locked, (screen.get_width() // 4 + 80, base_y + selected_p1 * spacing))
    if confirm_p2:
        locked = font.render("✓", True, (0, 255, 0))
        screen.blit(locked, (3 * screen.get_width() // 4 + 80, base_y + selected_p2 * spacing))

def character_selection_screen(screen, font):
    selected_p1 = 0
    selected_p2 = 1
    confirm_p1 = False
    confirm_p2 = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if not confirm_p1:
                    if event.key == pygame.K_w:
                        selected_p1 = (selected_p1 - 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_s:
                        selected_p1 = (selected_p1 + 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_q:
                        confirm_p1 = True

                if not confirm_p2:
                    if event.key == pygame.K_UP:
                        selected_p2 = (selected_p2 - 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_DOWN:
                        selected_p2 = (selected_p2 + 1) % len(CHARACTER_LIST)
                    elif event.key == pygame.K_RETURN:
                        confirm_p2 = True

                # Permitir desconfirmar
                if event.key == pygame.K_e:
                    confirm_p1 = False
                if event.key == pygame.K_BACKSPACE:
                    confirm_p2 = False

        # Evitar que elijan el mismo personaje
        if confirm_p1 and confirm_p2 and selected_p1 == selected_p2:
            confirm_p2 = False  # Forzar al segundo jugador a elegir otro
            # Podés mostrar un cartel si querés

        draw_character_select(screen, font, selected_p1, selected_p2, confirm_p1, confirm_p2)
        pygame.display.flip()
        clock.tick(60)

        if confirm_p1 and confirm_p2 and selected_p1 != selected_p2:
            break

    return CHARACTER_LIST[selected_p1], CHARACTER_LIST[selected_p2]
