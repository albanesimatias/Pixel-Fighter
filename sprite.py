import pygame
from constants import ID_Character, ID_Object, State, WIDTH, HEIGHT
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
        State.IDLE: self.load_sprites("assets/sprites/esteban/idle", size=(94*2, 64*2)),
        State.MOVE: self.load_sprites("assets/sprites/esteban/mover", size=(94*2, 64*2)),
        State.ATTACK: self.load_sprites("assets/sprites/esteban/atacar", size=(94*2, 64*2)),
        State.BLOCK: self.load_sprites("assets/sprites/esteban/bloquear", size=(94*2, 64*2)),
        State.KICKED: self.load_sprites("assets/sprites/esteban/daño", size=(94*2, 64*2)),
        State.DISTANCE_ATTACK: self.load_sprites("assets/sprites/esteban/lanzar", size=(94*2, 64*2))
      },
      ID_Object.BACKGROUND.value: { 0: self.load_sprites("assets/sprites/fondo", size=(WIDTH, HEIGHT)) },
      ID_Object.PROJECTILE.value: { 0: self.load_sprites("assets/sprites/proyectil", size=(64, 64)) }
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

    