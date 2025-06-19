import pygame
from personaje import Personaje  # Asumiendo que la clase está en personaje.py
import os

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 1024, 768
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Pelea - Demo")
fondo = pygame.image.load("assets/background.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Reloj para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Colores
NEGRO = (0, 0, 0)


def cargar_sprites_desde_carpeta(carpeta):
    sprites = []
    for archivo in sorted(os.listdir(carpeta)):
        ruta_completa = os.path.join(carpeta, archivo)
        imagen = pygame.image.load(ruta_completa).convert_alpha()
        sprites.append(imagen)
    return sprites


# Controles del jugador 1
controles_p1 = {
    'izquierda': pygame.K_a,
    'derecha': pygame.K_d,
    'arriba': pygame.K_w,
    'abajo': pygame.K_s,
    'atacar': pygame.K_f,
    'bloquear': pygame.K_g
}

sprites_ghost = {
    'idle': cargar_sprites_desde_carpeta("assets/sprites/idle"),
    'mover': cargar_sprites_desde_carpeta("assets/sprites/mover"),
    'atacar': cargar_sprites_desde_carpeta("assets/sprites/atacar"),
    'bloquear': cargar_sprites_desde_carpeta("assets/sprites/bloquear"),
}

# Crear personaje
jugador1 = Personaje(100, 400, sprites_ghost, controles_p1)

# Loop principal
ejecutando = True
while ejecutando:
    clock.tick(FPS)  # Limitar FPS

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Obtener teclas presionadas
    teclas = pygame.key.get_pressed()

    # Lógica del personaje
    jugador1.manejar_eventos(teclas)
    jugador1.actualizar()

    # Dibujar fondo
    pantalla.blit(fondo, (0, 0))

    # Dibujar personaje
    jugador1.dibujar(pantalla)

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
