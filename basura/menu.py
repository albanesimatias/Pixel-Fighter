import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Selección de Personajes")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 30)

# Lista de personajes
characters = ["estevan", "palomo"]
personajes_imagenes = [
    pygame.transform.scale(pygame.image.load("assets/char_select_estevan.jpg"), (100, 100)),
    pygame.transform.scale(pygame.image.load("assets/char_select_palomo.jpg"), (100, 100))
]

# Estado de selección
p1_index = 0
p2_index = 1
p1_confirmed = False
p2_confirmed = False

# Diccionario de controles
controles_j1 = {
    "izquierda": pygame.K_a,
    "derecha": pygame.K_d,
    "confirmar": pygame.K_RETURN
}

controles_j2 = {
    "izquierda": pygame.K_LEFT,
    "derecha": pygame.K_RIGHT,
    "confirmar": pygame.K_KP_ENTER
}


def manejar_seleccion(keys, index, confirmado, controles_jugador):
    """Actualiza la selección y confirmación del jugador"""
    if not confirmado:
        if keys[controles_jugador["izquierda"]]:
            index = (index - 1) % len(characters)
            pygame.time.wait(200)
        elif keys[controles_jugador["derecha"]]:
            index = (index + 1) % len(characters)
            pygame.time.wait(200)
        elif keys[controles_jugador["confirmar"]]:
            confirmado = True
    return index, confirmado


def draw_menu():
    screen.fill((30, 30, 30))
    title = FONT.render("Select your character", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    for i, name in enumerate(characters):
        x = 200 + i * 150
        y = HEIGHT // 2

        # Mostrar imagen en vez de rectángulo
        screen.blit(personajes_imagenes[i], (x, y))

        # Etiqueta del nombre
        label = FONT.render(name, True, (255, 255, 255))
        screen.blit(label, (x + 10, y + 160))

        # Marcos de selección
        marco = pygame.Rect(x, y, 100, 100)
        if i == p1_index:
            pygame.draw.rect(screen, (255, 0, 0), marco, 4)
        if i == p2_index:
            pygame.draw.rect(screen, (0, 0, 255), marco, 4)

    # Mensajes de confirmación
    if p1_confirmed:
        msg = FONT.render(f"Jugador 1 eligió: {characters[p1_index]}", True, (255, 0, 0))
        screen.blit(msg, (50, 500))

    if p2_confirmed:
        msg = FONT.render(f"Jugador 2 eligió: {characters[p2_index]}", True, (0, 0, 255))
        screen.blit(msg, (450, 500))

    pygame.display.flip()


# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Actualizar selección usando función
    p1_index, p1_confirmed = manejar_seleccion(keys, p1_index, p1_confirmed, controles_j1)
    p2_index, p2_confirmed = manejar_seleccion(keys, p2_index, p2_confirmed, controles_j2)

    draw_menu()
    clock.tick(60)

    if p1_confirmed and p2_confirmed:
        pygame.time.wait(1000)
        print("Jugador 1 eligió:", characters[p1_index])
        print("Jugador 2 eligió:", characters[p2_index])
        break
