import pygame
from Box2D.b2 import world
import os
from personaje import Personaje  # asumimos que guardaste la clase arriba aquí
from fondo import Fondo  # asumimos que guardaste la clase arriba aquí

pygame.init()
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pelea con Box2D")

clock = pygame.time.Clock()
FPS = 30

# Escala física
PPM = 30

# Crear mundo Box2D
mundo = world(gravity=(0, 30), doSleep=True)

# Suelo (estático)
suelo = mundo.CreateStaticBody(position=(ANCHO / 2 / PPM, ALTO / PPM))
suelo.CreatePolygonFixture(box=(ANCHO / 2 / PPM, 0.5), density=0, friction=0.8)

# Cargar sprites


def cargar_sprites_desde_carpeta(ruta, tamaño=None):
    sprites = []
    for archivo in sorted(os.listdir(ruta)):
        if archivo.endswith(".png") or archivo.endswith(".jpg"):
            imagen = pygame.image.load(os.path.join(ruta, archivo)).convert_alpha()
            if tamaño:
                imagen = pygame.transform.scale(imagen, tamaño)
            sprites.append(imagen)
    return sprites


sprites = {
    'idle': cargar_sprites_desde_carpeta("assets/sprites/idle", tamaño=(94*2, 64*2)),
    'mover': cargar_sprites_desde_carpeta("assets/sprites/mover", tamaño=(94*2, 64*2)),
    'atacar': cargar_sprites_desde_carpeta("assets/sprites/atacar", tamaño=(94*2, 64*2)),
    'bloquear': cargar_sprites_desde_carpeta("assets/sprites/bloquear", tamaño=(94*2, 64*2)),
    'dañado': cargar_sprites_desde_carpeta("assets/sprites/daño", tamaño=(94*2, 64*2))
}

background_sprites = cargar_sprites_desde_carpeta("assets/sprites/fondo", tamaño=(ANCHO, ALTO))

controles = {
    "izquierda": pygame.K_a,
    "derecha": pygame.K_d,
    "arriba": pygame.K_w,
    "abajo": pygame.K_s,
    "atacar": pygame.K_f,
    "bloquear": pygame.K_g
}

controles2 = {
    "izquierda": pygame.K_LEFT,
    "derecha": pygame.K_RIGHT,
    "arriba": pygame.K_UP,
    "abajo": pygame.K_DOWN,
    "atacar": pygame.K_RCTRL,
    "bloquear": pygame.K_g
}

jugador = Personaje(mundo, 100, 100, sprites, controles)
jugador2 = Personaje(mundo, 300, 100, sprites, controles2, nombre='Jugador2')
fondo = Fondo(background_sprites, tiempo_entre_frames=200)


# Loop principal
ejecutando = True
while ejecutando:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    jugador.manejar_eventos(teclas)
    jugador2.manejar_eventos(teclas)

    # Avanzar física
    mundo.Step(1.0 / FPS, 6, 2)

    jugador.actualizar()
    jugador2.actualizar()
    jugador.chequear_golpe(jugador2)
    jugador2.chequear_golpe(jugador)
    jugador.actualizar_direccion_personaje(jugador2)
    jugador2.actualizar_direccion_personaje(jugador)

    # Dibujar
    fondo.actualizar()
    fondo.dibujar(pantalla)
    jugador.dibujar(pantalla)
    jugador2.dibujar(pantalla)

    if jugador2.vida <= 0 or jugador.vida <= 0:
        Ganador = jugador.nombre if jugador.vida > 0 else jugador2.nombre
        print(f"El ganador es: {Ganador}")
        ejecutando = False
    pygame.display.flip()

pygame.quit()
