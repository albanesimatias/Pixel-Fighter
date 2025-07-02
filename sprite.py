import pygame
from constants import ID_Character, ID_Object, State, WIDTH, HEIGHT, ID_Scene, SPRITES_SIZE, Scene
import os

class Sprite:
    _instance = None

    @staticmethod
    def get_instance():
        if Sprite._instance is None:
            Sprite()
        return Sprite._instance

    def __init__(self):
        if Sprite._instance is not None:
            raise Exception("Esta clase es un singleton. Usa get_instance().")

        Sprite._instance = self

        self.sprites = {}
        self.load_assets()

    def load_sprites(self, path, size=None):
        sprites = []
        for file in sorted(os.listdir(path)):
            if file.endswith(".png") or file.endswith(".jpg"):
                image = pygame.image.load(os.path.join(path, file)).convert_alpha()
                if size:
                    image = pygame.transform.scale(image, size)
                sprites.append(image)
        return sprites

    def load_assets(self):
        self.sprites = {
            ID_Character.ESTEBAN.value: {
                State.IDLE: self.load_sprites("assets/sprites/esteban/idle", SPRITES_SIZE),
                State.MOVE: self.load_sprites("assets/sprites/esteban/mover", SPRITES_SIZE),
                State.ATTACK: self.load_sprites("assets/sprites/esteban/atacar", SPRITES_SIZE),
                State.BLOCK: self.load_sprites("assets/sprites/esteban/bloquear", SPRITES_SIZE),
                State.KICKED: self.load_sprites("assets/sprites/esteban/daño", SPRITES_SIZE),
                State.DISTANCE_ATTACK: self.load_sprites("assets/sprites/esteban/lanzar", SPRITES_SIZE),
                ID_Object.PROJECTILE: self.load_sprites("assets/sprites/esteban/proyectil", size=(64, 64))
            },
            ID_Character.MAXIMO.value: {
                State.IDLE: self.load_sprites("assets/sprites/maximo/idle", SPRITES_SIZE),
                State.MOVE: self.load_sprites("assets/sprites/maximo/mover", SPRITES_SIZE),
                State.ATTACK: self.load_sprites("assets/sprites/maximo/atacar", SPRITES_SIZE),
                State.BLOCK: self.load_sprites("assets/sprites/maximo/bloquear", SPRITES_SIZE),
                State.KICKED: self.load_sprites("assets/sprites/maximo/daño", SPRITES_SIZE),
                State.DISTANCE_ATTACK: self.load_sprites("assets/sprites/maximo/lanzar", SPRITES_SIZE),
                ID_Object.PROJECTILE: self.load_sprites("assets/sprites/maximo/proyectil", size=(25, 28)),
            },
            ID_Character.MARIANO.value: {
                State.IDLE: self.load_sprites("assets/sprites/mariano/idle",SPRITES_SIZE),
                State.MOVE: self.load_sprites("assets/sprites/mariano/mover", SPRITES_SIZE),
                State.ATTACK: self.load_sprites("assets/sprites/mariano/atacar", SPRITES_SIZE),
                State.BLOCK: self.load_sprites("assets/sprites/mariano/bloquear", SPRITES_SIZE),
                State.KICKED: self.load_sprites("assets/sprites/mariano/daño", SPRITES_SIZE),
                State.DISTANCE_ATTACK: self.load_sprites("assets/sprites/mariano/lanzar", SPRITES_SIZE),
                ID_Object.PROJECTILE: self.load_sprites("assets/sprites/mariano/proyectil", size=(64, 64))
            },
            ID_Character.MATIAS.value: {
                State.IDLE: self.load_sprites("assets/sprites/matias/idle", SPRITES_SIZE),
                State.MOVE: self.load_sprites("assets/sprites/matias/mover", SPRITES_SIZE),
                State.ATTACK: self.load_sprites("assets/sprites/matias/atacar", SPRITES_SIZE),
                State.BLOCK: self.load_sprites("assets/sprites/matias/bloquear", SPRITES_SIZE),
                State.KICKED: self.load_sprites("assets/sprites/matias/daño", SPRITES_SIZE),
                State.DISTANCE_ATTACK: self.load_sprites("assets/sprites/matias/lanzar", SPRITES_SIZE),
                ID_Object.PROJECTILE: self.load_sprites("assets/sprites/matias/proyectil", size=(30, 30))
            },
            ID_Object.BACKGROUND.value: {
                Scene.INTRO:  self.load_sprites("assets/sprites/fondo/intro", size=(WIDTH, HEIGHT)),
                Scene.FIGHT: self.load_sprites("assets/sprites/fondo/fight", size=(WIDTH, HEIGHT)),
                Scene.SELECT: self.load_sprites("assets/sprites/fondo/select", size=(WIDTH, HEIGHT))
            },
            ID_Scene.WIN.value: {
                ID_Character.ESTEBAN.value: self.load_sprites("assets/sprites/esteban/win", size=(WIDTH/2, HEIGHT/2)),
                ID_Character.MARIANO.value: self.load_sprites("assets/sprites/mariano/win", size=(WIDTH/2, HEIGHT/2)),
                ID_Character.MAXIMO.value: self.load_sprites("assets/sprites/maximo/win", size=(WIDTH/2, HEIGHT/2)),
                ID_Character.MATIAS.value: self.load_sprites("assets/sprites/matias/win", size=(WIDTH/2, HEIGHT/2)),
                ID_Scene.EMPATE.value: self.load_sprites("assets/sprites/draw", size=(WIDTH/2, HEIGHT/2))
            }
        }

    def get_sprite(self, id, state):
        return self.sprites.get(id, {}).get(state, [])

    def get_sprite_len(self, id, state):
        return len(self.get_sprite(id, state))

    def get_sprite_frame(self, id, state, index):
        try:
            return self.get_sprite(id, state)[index]
        except IndexError:
            print(f"[ERROR] Frame index fuera de rango: id={id}, state={state}, index={index}")
            return None
        except Exception as e:
            print(f"[ERROR] al obtener sprite frame: {e}")
            return None
