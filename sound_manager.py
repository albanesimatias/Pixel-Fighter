import pygame
from constants import *


class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {
            Sound.ATTACK: pygame.mixer.Sound("assets/sounds/attack.wav"),
            Sound.JUMP: pygame.mixer.Sound("assets/sounds/jump_grave.wav"),
            Sound.BLOCKED: pygame.mixer.Sound("assets/sounds/block.wav"),
            Sound.KICKED: pygame.mixer.Sound("assets/sounds/kicked.wav"),
            Sound.LOOP: pygame.mixer.Sound("assets/sounds/loop_sound.wav"),
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

    def play_music(self, sound_name: str):
        def decorator(func):
            def wrapper(*args, **kwargs):
                sound = self.sounds.get(sound_name)
                sound.set_volume(VOLUME)
                if sound:
                    sound.play(loops=-1)
                try:
                    return func(*args, **kwargs)
                finally:
                    if sound:
                        sound.stop()
            return wrapper
        return decorator


sound_manager = SoundManager()
