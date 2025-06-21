import pygame
from Box2D.b2 import dynamicBody

PPM = 30  # pixeles por metro
WIDTH, HEIGHT = 100, 120  # dimensiones del sprite base


class Character:
    def __init__(self, world, x, y, sprites, controls, name='Jugador'):
        self.name = name
        self.hp = 100
        self.sprites = sprites
        self.controls = controls
        self.direction = 1
        self.state = 'idle'
        self.frame = 0
        self.cooldown_anim = 100
        self.last_update = pygame.time.get_ticks()
        self.in_animation = False
        self.in_air = False
        self.rect_hit = None
        self.has_attacked = False

        self.body = world.CreateDynamicBody(position=(x / PPM, y / PPM), fixedRotation=True)
        self.body.CreatePolygonFixture(box=(WIDTH/PPM/2, HEIGHT/PPM/2), density=1, friction=0.5)

        self.matriz_estados = {
            'idle': {
                'evt_left': self.move,
                'evt_right': self.move,
                'evt_up': self.jump,
                'evt_attack': self.attack,
                'evt_block': self.block,
                'evt_kicked': self.kicked,
            },
            'move': {
                'evt_idle': self.idle,
                'evt_attack': self.attack,
                'evt_up': self.jump,
                'evt_block': self.block,
                'evt_kicked': self.kicked,
            },
            'attack': {
                'evt_end_animation': self.idle
            },
            'block': {
                'evt_end_animation': self.idle,
                'evt_kicked': self.block_succesfull
            },
            'kicked': {
                'evt_end_animation': self.idle
            }
        }

    # === funciones de estado ===

    def idle(self):
        self.state = 'idle'
        self.frame = 0
        self.in_animation = False
        self.rect_hit = None

    def move(self):
        self.state = 'move'
        self.frame = 0
        self.in_animation = False
        self.rect_hit = None

    def attack(self):
        self.state = 'attack'
        self.frame = 0
        self.in_animation = True
        self.last_update = pygame.time.get_ticks()
        self.has_attacked = False
        # Se genera un rect de golpe temporal (zona de recive_damage)
        x = self.body.position.x * PPM
        y = self.body.position.y * PPM
        width = 40
        offset = 40 if self.direction == 1 else -135
        self.rect_hit = pygame.Rect(x + offset, y - 80, width, 40)

    def block(self):
        self.state = 'block'
        self.frame = 0
        self.in_animation = True
        self.last_update = pygame.time.get_ticks()
        self.rect_hit = None

    def recive_damage(self, damage):
        self.hp -= damage
        print(f"{self.name} recibió {damage} de recive_damage. hp restante: {self.hp}")

    def kicked(self):
        self.state = 'kicked'
        self.frame = 0
        self.in_animation = True
        self.last_update = pygame.time.get_ticks()
        self.rect_hit = None

    def block_succesfull(self):
        print(f"{self.name} bloqueó el ataque.")
        # Puede reproducir animación o simplemente seguir bloqueando

    def jump(self):
        if not self.in_air:
            self.body.ApplyLinearImpulse((0, -250), self.body.worldCenter, True)
            self.in_air = True

    def update_character_direction(self, rival):
        if rival.body.position.x > self.body.position.x:
            self.direction = 1   # mira a la derecha
        else:
            self.direction = -1  # mira a la izquierda

    # === Entrada de evento FSM ===

    def execute(self, evento):
        actions = self.matriz_estados.get(self.state, {})
        function = actions.get(evento)
        if function:
            function()

    # === Entrada del jugador ===

    def event_handler(self, key_words):
        if self.state in {'block', 'kicked'} and self.in_animation:
            return

        vel = self.body.linearVelocity
        new_vel = [0, vel.y]

        if key_words[self.controls['attack']]:
            self.execute('evt_attack')
            return

        if key_words[self.controls['block']]:
            self.execute('evt_block')
            return

        if key_words[self.controls['left']]:
            new_vel[0] = -7
            self.direction = -1
            self.execute('evt_left')

        if key_words[self.controls['right']]:
            new_vel[0] = 7
            self.direction = 1
            self.execute('evt_right')

        if key_words[self.controls['up']]:
            self.execute('evt_up')

        if not (key_words[self.controls['left']] or
                key_words[self.controls['right']] or
                key_words[self.controls['up']]):
            self.execute('evt_idle')

        self.body.linearVelocity = (new_vel[0], self.body.linearVelocity.y)

    # === Verificación de colisiones entre personajes ===

    def hit_check(self, enemy):
        if self.state == 'attack' and self.rect_hit and not self.has_attacked:
            rect_otro = enemy.get_rect()
            if self.rect_hit.colliderect(rect_otro):
                enemy.execute('evt_kicked')
                if enemy.state != 'block':
                    enemy.recive_damage(10)
                else:
                    enemy.block_succesfull()
                self.has_attacked = True

    # === Posición física ===

    def get_rect(self):
        x = int(self.body.position.x * PPM)
        y = int(self.body.position.y * PPM)
        return pygame.Rect(x - 60, y - 128, 64, 128)

    # === Animación ===

    def update(self):
        if abs(self.body.linearVelocity.y) < 0.01:
            self.in_air = False

        now = pygame.time.get_ticks()
        if now - self.last_update >= self.cooldown_anim:
            self.last_update = now
            self.frame += 1

            if self.frame >= len(self.sprites[self.state]):
                self.frame = 0
                if self.state in {'attack', 'block', 'kicked'}:
                    self.execute('evt_end_animation')

    def draw(self, screem):
        pos = self.body.position
        x = int(pos[0] * PPM)
        y = int(pos[1] * PPM)

        image = self.sprites[self.state][self.frame]
        if self.direction == -1:
            image = pygame.transform.flip(image, True, False)

        width_sprite = image.get_width()
        alto_sprite = image.get_height()

        # Centramos horizontalmente y dibujamos desde los pies
        screem.blit(image, (x - width_sprite // 2, y - alto_sprite))

        # Dibujo de hitbox de ataque (debug)
        # if self.rect_hit:
        #    pygame.draw.rect(screem, (255, 0, 0), self.rect_hit, 1)
