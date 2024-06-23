import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
import random
from weapon import Weapon
from enemy import Enemy
from particles import ParticlesFrameStorage

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_weapon = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.particle_frame_storage = ParticlesFrameStorage()

        self.create_map()

    def create_map(self):
        layouts = {'boundary': import_csv_layout(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\layers\boundaries.csv'),
                   'grass': import_csv_layout(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\layers\grass.csv'),
                   'objects': import_csv_layout(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\layers\objects.csv'),
                   'entities': import_csv_layout(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\layers\entities.csv')}
        graphics = {'grass': import_graphics(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\grass'),
                   'objects': import_graphics(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\graphics\objects')}
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1': 
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                                Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'grass':
                                random_grass_image = random.choice(graphics[style])
                                Tile((x,y),[self.obstacle_sprites,self.visible_sprites,self.attackable_sprites],'grass',random_grass_image)
                        if style == 'objects':
                                object_image = graphics[style][int(col)]
                                Tile((x,y),[self.obstacle_sprites,self.visible_sprites],'object',object_image)
                        if style == 'entities':
                                if col == '0': 
                                    self.player = Player((x,y),
                                                         [self.visible_sprites],
                                                         self.obstacle_sprites,
                                                         self.create_weapon,
                                                         self.destroy_weapon)
                                else:
                                    Enemy(col,
                                          (x,y),
                                          [self.visible_sprites,self.attackable_sprites],
                                          self.obstacle_sprites,self.damage_player,self.trigger_enemy_death)

    def create_weapon(self):
        self.current_weapon = Weapon(self.player,[self.visible_sprites,self.attack_sprites],self.player_attack_check)

    def destroy_weapon(self):
        self.current_weapon.kill()

    def player_attack_check(self):
         if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                for sprite in collision_sprites:
                    if sprite.sprite_type == 'grass':
                        sprite.kill()
                    else:
                         sprite.get_damage(self.player,attack_sprite.attack_type)
    
    def damage_player(self,amount,attack_type):
         if self.player.vulnerable:   
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particles

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        # debug()
        self.visible_sprites.enemy_update(self.player)
        
    def trigger_enemy_death(self,enemy_name,pos):
         self.particle_frame_storage.death_particles(enemy_name,pos,self.visible_sprites)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        # creating the floor
        self.floor_surface = pygame.image.load(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\tilemap\tiled project\Hyrule.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        
    def custom_draw(self,player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self,player):
         enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
         for enemy in enemy_sprites:
              enemy.enemy_update(player)