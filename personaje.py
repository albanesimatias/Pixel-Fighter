import pygame


class Personaje:
    def __init__(self, x, y, sprites, controles):
        """
        sprites: dict con keys: 'idle', 'mover', 'atacar', 'bloquear'
                 Cada valor debe ser una lista de imágenes (frames de animación).
        controles: dict con keys: 'izquierda', 'derecha', 'arriba', 'abajo', 'atacar', 'bloquear'
        """
        self.x = x
        self.y = y
        self.sprites = sprites
        self.controles = controles

        self.estado = 'idle'
        self.frame = 0
        self.velocidad = 5
        self.direccion = 1  # 1: derecha, -1: izquierda

        self.rect = pygame.Rect(self.x, self.y, 64, 64)  # ajustar según tamaño de sprite

        # Temporizador para animación
        self.ultimo_update = pygame.time.get_ticks()
        self.cooldown_anim = 100  # milisegundos entre frames

    def manejar_eventos(self, teclas):
        if teclas[self.controles['bloquear']]:
            self.bloquear()
        elif teclas[self.controles['atacar']]:
            self.atacar()
        else:
            self.mover(teclas)

    def mover(self, teclas):
        self.estado = 'idle'
        if teclas[self.controles['izquierda']]:
            self.x -= self.velocidad
            self.direccion = -1
            self.estado = 'mover'
        elif teclas[self.controles['derecha']]:
            self.x += self.velocidad
            self.direccion = 1
            self.estado = 'mover'

        if teclas[self.controles['arriba']]:
            self.y -= self.velocidad
            self.estado = 'mover'
        elif teclas[self.controles['abajo']]:
            self.y += self.velocidad
            self.estado = 'mover'

        self.rect.topleft = (self.x, self.y)

    def atacar(self):
        self.estado = 'atacar'

    def bloquear(self):
        self.estado = 'bloquear'

    def actualizar(self):
        # Actualizar animación por estado
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_update >= self.cooldown_anim:
            self.ultimo_update = tiempo_actual
            self.frame = (self.frame + 1) % len(self.sprites[self.estado])

    def dibujar(self, pantalla):
        imagen = self.sprites[self.estado][self.frame]
        if self.direccion == -1:
            imagen = pygame.transform.flip(imagen, True, False)
        pantalla.blit(imagen, (self.x, self.y))
