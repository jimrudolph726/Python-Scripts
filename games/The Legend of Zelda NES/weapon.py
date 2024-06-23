import pygame
from support import import_graphics
from settings import weapon_data
import random

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups,player_attack_check):
        super().__init__(groups)
        direction = player.status.split('_')[0]
        self.attack_type = 'weapon'
        self.player_attack_check = player_attack_check
        self.damage = weapon_data[player.weapon]['damage']

        self.image = pygame.image.load(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\weapons\{player.weapon}\{direction}.png').convert_alpha()
        if direction == 'up': 
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-7,10))
        if direction == 'down': 
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(5,-5))
        if direction == 'left': 
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(11,3))
        if direction == 'right': 
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-11,3))
            
        self.player_attack_check()
    
    # def import_weapons(self):
    #     weapon_animation_path = fr'graphics/weapons/'
    #     animations = {'sword':[]}
    #     for key in animations.keys():
    #         full_path = weapon_animation_path + str(key)
    #         animations[key] = import_graphics(full_path)
    #     self.weapon_images = {
    #         'down': animations['sword'][0],
    #         'left': animations['sword'][1],
    #         'right': animations['sword'][2],
    #         'up': animations['sword'][3]
    #     }
    #     self.image = self.weapon_images[self.direction]





