import pygame


class Fondo:
    def __init__(self, frames, tiempo_entre_frames=200):
        self.frames = frames
        print(self.frames)
        self.indice_frame = 0
        self.tiempo_entre_frames = tiempo_entre_frames
        self.ultimo_cambio = pygame.time.get_ticks()

    def actualizar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_cambio > self.tiempo_entre_frames:
            self.indice_frame = 0 if self.indice_frame == 1 else 1
            self.ultimo_cambio = ahora

    def dibujar(self, pantalla):
        pantalla.blit(self.frames[self.indice_frame], (0, 0))
