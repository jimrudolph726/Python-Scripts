import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
import random
from weapon import Weapon
from enemy import Enemy

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

        # attack sprites
        self.current_weapon = None
    
    def create_map(self):
        layouts = {'boundary': import_csv_layout(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\layers\boundaries.csv'),
                   'grass': import_csv_layout(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\layers\grass.csv'),
                   'objects': import_csv_layout(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\layers\objects.csv'),
                   'entities': import_csv_layout(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\layers\entities.csv')}
        graphics = {'grass': import_graphics(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\grass'),
                   'objects': import_graphics(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\objects')}
        
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
                            Tile((x,y),[self.obstacle_sprites,self.visible_sprites],'grass',random_grass_image)
                        if style == 'objects':
                            object_image = graphics[style][int(col)]
                            Tile((x,y),[self.obstacle_sprites,self.visible_sprites],'object',object_image)
                        if style == 'entities':
                            if col == '0': 
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_weapon,self.destroy_weapon)
                            else:
                                Enemy(col,(x,y),[self.visible_sprites],self.obstacle_sprites)

    def create_weapon(self):
        self.current_weapon = Weapon(self.player,[self.visible_sprites])

    def destroy_weapon(self):
        if self.current_weapon:
            self.current_weapon.kill()
        self.current_weapon = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Load the floor surface
        self.floor_surface = pygame.image.load(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\tilemap\tiled project\Hyrule.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        
        # Create tiles
        self.tiles = self.load_tiles()

    def load_tiles(self):
        tile_size = 512  # Size of each tile
        tiles = []
        for x in range(0, self.floor_rect.width, tile_size):
            row = []
            for y in range(0, self.floor_rect.height, tile_size):
                tile_surface = pygame.Surface((tile_size, tile_size))
                tile_surface.blit(self.floor_surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
                row.append(tile_surface)
            tiles.append(row)
        return tiles

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        start_x = max(int(self.offset.x // 512), 0)
        start_y = max(int(self.offset.y // 512), 0)
        end_x = min(start_x + int(self.display_surface.get_width() // 512) + 2, len(self.tiles))
        end_y = min(start_y + int(self.display_surface.get_height() // 512) + 2, len(self.tiles[0]))

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                offset_pos = pygame.math.Vector2(x * 512, y * 512) - self.offset
                self.display_surface.blit(self.tiles[x][y], offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
