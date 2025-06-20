import pygame
from Box2D.b2 import dynamicBody

PPM = 30  # pixeles por metro


class Personaje:
    def __init__(self, mundo, x, y, sprites, controles, nombre='Jugador'):
        self.nombre = nombre
        self.vida = 100
        self.sprites = sprites
        self.controles = controles
        self.direccion = 1
        self.estado_actual = 'idle'
        self.frame = 0
        self.cooldown_anim = 100
        self.ultimo_update = pygame.time.get_ticks()
        self.en_animacion = False
        self.en_el_aire = False
        self.rect_golpe = None
        self.ya_golpeo = False

        self.body = mundo.CreateDynamicBody(position=(x / PPM, y / PPM), fixedRotation=True)
        self.body.CreatePolygonFixture(box=(0.5, 1), density=1, friction=0.5)

        self.matriz_estados = {
            'idle': {
                'presiona_izq': self.mover,
                'presiona_der': self.mover,
                'presiona_arriba': self.saltar,
                'presiona_ataque': self.atacar,
                'presiona_bloqueo': self.bloquear,
                'recibir_golpe': self.dañado,
            },
            'mover': {
                'sueltateclas': self.idle,
                'presiona_ataque': self.atacar,
                'presiona_arriba': self.saltar,
                'presiona_bloqueo': self.bloquear,
                'recibir_golpe': self.dañado,
            },
            'atacar': {
                'fin_anim': self.idle
            },
            'bloquear': {
                'fin_anim': self.idle,
                'recibir_golpe': self.bloqueo_exitoso
            },
            'dañado': {
                'fin_anim': self.idle
            }
        }

    # === Funciones de estado ===

    def idle(self):
        self.estado_actual = 'idle'
        self.frame = 0
        self.en_animacion = False
        self.rect_golpe = None

    def mover(self):
        self.estado_actual = 'mover'
        self.frame = 0
        self.en_animacion = False
        self.rect_golpe = None

    def atacar(self):
        self.estado_actual = 'atacar'
        self.frame = 0
        self.en_animacion = True
        self.ultimo_update = pygame.time.get_ticks()
        self.ya_golpeo = False
        # Se genera un rect de golpe temporal (zona de daño)
        x = self.body.position.x * PPM
        y = self.body.position.y * PPM
        ancho = 40
        offset = 40 if self.direccion == 1 else -80
        self.rect_golpe = pygame.Rect(x + offset, y - 80, ancho, 40)

    def bloquear(self):
        self.estado_actual = 'bloquear'
        self.frame = 0
        self.en_animacion = True
        self.ultimo_update = pygame.time.get_ticks()
        self.rect_golpe = None

    def daño(self, cantidad):
        self.vida -= cantidad
        print(f"{self.nombre} recibió {cantidad} de daño. Vida restante: {self.vida}")

    def dañado(self):
        self.estado_actual = 'dañado'
        self.frame = 0
        self.en_animacion = True
        self.ultimo_update = pygame.time.get_ticks()
        self.rect_golpe = None

    def bloqueo_exitoso(self):
        print(f"{self.nombre} bloqueó el ataque.")
        # Puede reproducir animación o simplemente seguir bloqueando

    def saltar(self):
        if not self.en_el_aire:
            self.body.ApplyLinearImpulse((0, -30), self.body.worldCenter, True)
            self.en_el_aire = True

    def actualizar_direccion_personaje(self, rival):
        if rival.body.position.x > self.body.position.x:
            self.direccion = 1   # mira a la derecha
        else:
            self.direccion = -1  # mira a la izquierda

    # === Entrada de evento FSM ===

    def procesar_evento(self, evento):
        acciones = self.matriz_estados.get(self.estado_actual, {})
        funcion = acciones.get(evento)
        if funcion:
            funcion()

    # === Entrada del jugador ===

    def manejar_eventos(self, teclas):
        if self.estado_actual in {'bloquear', 'dañado'} and self.en_animacion:
            return

        vel = self.body.linearVelocity
        nueva_vel = [0, vel.y]

        if teclas[self.controles['atacar']]:
            self.procesar_evento('presiona_ataque')
            return

        if teclas[self.controles['bloquear']]:
            self.procesar_evento('presiona_bloqueo')
            return

        if teclas[self.controles['izquierda']]:
            nueva_vel[0] = -7
            self.direccion = -1
            self.procesar_evento('presiona_izq')

        if teclas[self.controles['derecha']]:
            nueva_vel[0] = 7
            self.direccion = 1
            self.procesar_evento('presiona_der')

        if teclas[self.controles['arriba']]:
            self.procesar_evento('presiona_arriba')

        if not (teclas[self.controles['izquierda']] or
                teclas[self.controles['derecha']] or
                teclas[self.controles['arriba']]):
            self.procesar_evento('sueltateclas')

        self.body.linearVelocity = (nueva_vel[0], self.body.linearVelocity.y)

    # === Verificación de colisiones entre personajes ===

    def chequear_golpe(self, otro_personaje):
        if self.estado_actual == 'atacar' and self.rect_golpe and not self.ya_golpeo:
            rect_otro = otro_personaje.get_rect()
            if self.rect_golpe.colliderect(rect_otro):
                otro_personaje.procesar_evento('recibir_golpe')
                if otro_personaje.estado_actual != 'bloquear':
                    otro_personaje.daño(10)
                else:
                    otro_personaje.bloqueo_exitoso()
                self.ya_golpeo = True

    # === Posición física ===

    def get_rect(self):
        x = int(self.body.position.x * PPM)
        y = int(self.body.position.y * PPM)
        return pygame.Rect(x - 32, y - 128, 64, 128)

    # === Animación ===

    def actualizar(self):
        if abs(self.body.linearVelocity.y) < 0.01:
            self.en_el_aire = False

        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_update >= self.cooldown_anim:
            self.ultimo_update = ahora
            self.frame += 1

            if self.frame >= len(self.sprites[self.estado_actual]):
                self.frame = 0
                if self.estado_actual in {'atacar', 'bloquear', 'dañado'}:
                    self.procesar_evento('fin_anim')

    def dibujar(self, pantalla):
        pos = self.body.position
        x = int(pos[0] * PPM)
        y = int(pos[1] * PPM)

        imagen = self.sprites[self.estado_actual][self.frame]
        if self.direccion == -1:
            imagen = pygame.transform.flip(imagen, True, False)

        ancho_sprite = imagen.get_width()
        alto_sprite = imagen.get_height()

        # Centramos horizontalmente y dibujamos desde los pies
        pantalla.blit(imagen, (x - ancho_sprite // 2, y - alto_sprite))

        # Dibujo de hitbox de ataque (debug)
        if self.rect_golpe:
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect_golpe, 1)
