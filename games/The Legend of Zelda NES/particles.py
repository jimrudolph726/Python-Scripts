import pygame
from settings import *
from support import import_graphics

class ParticlesFrameStorage:
    def __init__(self):
        self.frames = {'red_darknut': import_graphics(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\particles\red_darknut')}

    def death_particles(self,enemy_name,pos,groups):
        death_graphics = self.frames[enemy_name]

        DeathParticles(pos,groups,death_graphics)

class DeathParticles(pygame.sprite.Sprite):
    def __init__(self,pos,groups,death_graphics):
        # General setup
        super().__init__(groups)

        self.animation_speed = 0.2
        self.pos = pos
        self.frame_index = 0  # Initialize frame_index
        self.death_graphics = death_graphics

        # Graphics setup
        self.image = self.death_graphics[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.death_graphics):
            self.kill()
        else:
            self.image = self.death_graphics[int(self.frame_index)]
            

    def update(self):
        self.animate()