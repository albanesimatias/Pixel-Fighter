import pygame
from constants import *
from sprite import Sprite
from sound_manager import sound_manager

from projectile import Projectile


class Character:
    def __init__(self, world, x, y, controls, name=ID_Character.ESTEBAN.value):
        self.name = name
        self.hp = CHARACTER_HP
        self.controls = controls
        self.direction = Direction.LEFT
        self.state = State.IDLE
        self.frame = 0
        self.cooldown_anim = COOLDOWN_ANIM
        self.last_update = pygame.time.get_ticks()
        self.in_animation = False
        self.in_air = False
        self.rect_hit = None
        self.has_attacked = False

        self.projectiles = []
        self.last_shot_time = 0
        self.shoot_cooldown = SHOOT_COOLDDOWN

        self.attack_cooldown = ATTACK_COOLDOWN
        self.last_attack_time = 0

        self.body = world.CreateDynamicBody(position=(x / PPM, y / PPM), fixedRotation=True)
        self.body.CreatePolygonFixture(box=(WIDTH_SPRITE/PPM/2, HEIGHT_SPRITE/PPM/2), density=DENSITY, friction=FRICTION)

        self.matriz_estados = {
            State.IDLE: {
                'evt_left': self.move,
                'evt_right': self.move,
                'evt_up': self.can_jump,
                'evt_attack': self.can_attack,
                'evt_block': self.block,
                'evt_kicked': self.kicked,
            },
            State.MOVE: {
                'evt_idle': self.idle,
                'evt_attack': self.can_attack,
                'evt_up': self.can_jump,
                'evt_block': self.block,
                'evt_kicked': self.kicked,
            },
            State.ATTACK: {
                'evt_end_animation': self.idle
            },
            State.BLOCK: {
                'evt_kicked': self.block_succesfull,
                'evt_attack': self.can_attack,
                'evt_block': self.block,
                'evt_left': self.move,
                'evt_right': self.move,
                'evt_up': self.can_jump,
            },
            State.KICKED: {
                'evt_end_animation': self.idle
            },
            State.DISTANCE_ATTACK: {
                'evt_end_animation': self.idle
            },
        }

    def idle(self):
        self.state = State.IDLE
        self.frame = 0
        self.in_animation = False
        self.rect_hit = None

    def move(self):
        self.state = State.MOVE
        self.frame = 0
        self.in_animation = False
        self.rect_hit = None

    @sound_manager.play_sound(Sound.ATTACK, True)
    def attack(self, now):
        self.last_attack_time = now
        self.state = State.ATTACK
        self.frame = 0
        self.in_animation = True
        self.last_update = pygame.time.get_ticks()
        self.has_attacked = False

        x = self.body.position.x * PPM
        y = self.body.position.y * PPM

        offset = CHARACTER_WIDTH if self.direction == Direction.RIGHT else -135
        self.rect_hit = pygame.Rect(x + offset, y - 80, CHARACTER_WIDTH, 40)

    def can_attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time < self.attack_cooldown:
            return

        self.attack(now)

    def block(self):
        self.state = State.BLOCK
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.rect_hit = None

    def recive_damage(self, damage):
        self.hp -= damage

    @sound_manager.play_sound(Sound.KICKED)
    def kicked(self):
        self.state = State.KICKED
        self.frame = 0
        self.in_animation = True
        self.last_update = pygame.time.get_ticks()
        self.rect_hit = None

    @sound_manager.play_sound(Sound.BLOCKED)
    def block_succesfull(self):
        pass

    @sound_manager.play_sound(Sound.JUMP, True)
    def jump(self):
        self.body.ApplyLinearImpulse((0, -250), self.body.worldCenter, True)
        self.in_air = True

    def can_jump(self):
        if not self.in_air:
            self.jump()

    def shoot(self):
        now = pygame.time.get_ticks()
        offset = 1 if self.direction == Direction.RIGHT else -1
        if now - self.last_shot_time >= self.shoot_cooldown:
            self.state = State.DISTANCE_ATTACK
            self.in_animation = True
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            x = self.body.position.x + offset
            y = self.body.position.y - 2
            self.projectiles.append(Projectile(self.body.world, x, y, self.direction, Sprite.get_instance().get_sprite_frame(self.name, ID_Object.PROJECTILE, 0), self.body.position.y))
            self.last_shot_time = now

    def update_character_direction(self, rival):
        if rival.body.position.x > self.body.position.x:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.LEFT

    def execute(self, evento):
        actions = self.matriz_estados.get(self.state, {})
        function = actions.get(evento)
        if function:
            function()

    def event_handler(self, key_words):
        if self.state in {State.BLOCK, State.KICKED, State.DISTANCE_ATTACK} and self.in_animation:
            return

        vel = self.body.linearVelocity
        new_vel = [0, vel.y]

        if key_words[self.controls['attack']]:
            self.execute('evt_attack')
            return

        if key_words[self.controls['block']]:
            self.execute('evt_block')
            return

        if key_words[self.controls['down']]:
            self.shoot()
            return

        if key_words[self.controls['left']]:
            new_vel[0] = -7
            self.direction = Direction.LEFT
            self.execute('evt_left')

        if key_words[self.controls['right']]:
            new_vel[0] = 7
            self.direction = Direction.RIGHT
            self.execute('evt_right')

        if key_words[self.controls['up']]:
            self.execute('evt_up')

        if not (key_words[self.controls['left']] or
                key_words[self.controls['right']] or
                key_words[self.controls['up']]):
            self.execute('evt_idle')

        self.body.linearVelocity = (new_vel[0], self.body.linearVelocity.y)

    def hit_check(self, enemy):
        if self.state == State.ATTACK and self.rect_hit and not self.has_attacked:
            rect_otro = enemy.get_rect()
            if self.rect_hit.colliderect(rect_otro):
                enemy.execute('evt_kicked')
                if enemy.state != State.BLOCK:
                    enemy.recive_damage(10)
                else:
                    enemy.block_succesfull()
                self.has_attacked = True

    def projectile_hit_check(self, enemy):
        for proj in self.projectiles:
            if proj.alive:
                rect_proj = pygame.Rect(
                    int(proj.body.position.x * PPM) - 6,
                    int(proj.body.position.y * PPM) - 6,
                    12, 12
                )
                if rect_proj.colliderect(enemy.get_rect()):
                    proj.alive = False
                    enemy.execute('evt_kicked')
                    if enemy.state != State.BLOCK:
                        enemy.recive_damage(5)
                    else:
                        enemy.block_succesfull()

    def get_rect(self):
        x = int(self.body.position.x * PPM)
        y = int(self.body.position.y * PPM)
        return pygame.Rect(x - 60, y - 128, 64, 128)

    def update(self):
        if abs(self.body.linearVelocity.y) < 0.01:
            self.in_air = False

        now = pygame.time.get_ticks()
        if now - self.last_update >= self.cooldown_anim:
            self.last_update = now
            self.frame += 1

            if self.frame >= Sprite.get_instance().get_sprite_len(self.name, self.state):
                self.frame = 0
                if self.state in {State.ATTACK, State.KICKED, State.DISTANCE_ATTACK}:
                    self.execute('evt_end_animation')

        for proj in self.projectiles:
            proj.update()
        self.projectiles = [p for p in self.projectiles if p.alive]

    def draw(self, screen):
        pos = self.body.position
        x = int(pos[0] * PPM)
        y = int(pos[1] * PPM)

        image = Sprite.get_instance().get_sprite_frame(self.name, self.state, self.frame)
        if self.direction == Direction.LEFT:
            image = pygame.transform.flip(image, True, False)

        width_sprite = image.get_width()
        alto_sprite = image.get_height()

        screen.blit(image, (x - width_sprite // 2, y - alto_sprite))

        for proj in self.projectiles:
            proj.draw(screen)
