import pygame
from constants import Sound

class SoundManager:
  def __init__(self):
    pygame.mixer.init()

    self.sounds = {
        Sound.ATTACK: pygame.mixer.Sound("assets/sounds/attack.wav"),
        Sound.JUMP: pygame.mixer.Sound("assets/sounds/jump.wav"),
    }

  def play_sound(self, sound_name: str, play_before=False):
    def decorator(func):
      def wrapper(*args, **kwargs):
        sound = self.sounds.get(sound_name)
        if play_before and sound:
            sound.play()
        result = func(*args, **kwargs)
        if not play_before and sound:
            sound.play()
        return result
      return wrapper
    return decorator

sound_manager = SoundManager()