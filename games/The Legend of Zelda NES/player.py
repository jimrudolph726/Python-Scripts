import pygame
from settings import *
from support import import_graphics
import random
from ui import ui
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_weapon,destroy_weapon):
        super().__init__(groups)
        self.status = 'down_idle'
        self.image = pygame.image.load(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\link\{self.status}\1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.sword_sound = pygame.mixer.Sound(fr'C:\Users\jimru\Desktop\zelda_nes\sound\sword.mp3')
        self.vulnerable = True
        

        # graphics setup
        self.import_link_animations()
        
        # movement
        self.attacking = False
        self.attack_time = None
        self.can_attack = True
        self.hurt_time = None
        self.invincibility_duration = 500

        # weapon
        self.create_weapon = create_weapon
        self.destroy_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.attack_cooldown = 400
        self.weapon_cooldown = weapon_data[self.weapon]['weapon_cooldown']
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.weapon_switch_cooldown = 200

        # player stats
        self.stats = {'health': 100, 'energy': 50, 'attack': 10, 'magic': 5, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.experience = 0
        self.speed = self.stats['speed']
        self.obstacle_sprites = obstacle_sprites

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_link_animations(self):
        link_animation_path = fr'C:\Users\jimru\Desktop\zelda_nes\graphics\link'
        self.animations = {'up':[],'down':[],'left':[],'right':[],
                            'up_idle':[],'down_idle':[],'left_idle':[],'right_idle':[],
                            'up_attack':[],'down_attack':[],'left_attack':[],'right_attack':[],}
        for key in self.animations.keys():
            full_path = link_animation_path + "/" + str(key)
            self.animations[key] = import_graphics(full_path)
        
    def input(self):
        if self.attacking == False:
            # movement input
            keys = pygame.key.get_pressed()

            self.direction = pygame.math.Vector2()
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1 
                self.status = 'right'
            else:
                self.direction.x = 0

            if self.direction.x != 0:
                self.direction.y = 0
            if self.direction.y != 0:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.can_attack = False
                self.create_weapon()
                self.sword_sound.play()

            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
        
            # weapon selection input
            if keys[pygame.K_q] and self.can_switch_weapon == True:
                
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(list(weapon_data.keys())):
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
                self.attack_cooldown = weapon_data[self.weapon]['weapon_cooldown']
                    
    def animate(self):
        # link is not moving

        if self.direction.x == 0 and self.direction.y == 0:
            if '_idle' not in self.status: 
                if '_attack' not in self.status:
                    self.status += '_idle'
                else:
                    self.status = self.status.replace('_attack','_idle')
            
        if self.attacking == True:
            self.direction.x == 0
            self.direction.y == 0
            if '_attack' not in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status += '_attack'

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):

        current_time = pygame.time.get_ticks()
        if self.attack_time is not None:
            if current_time - self.attack_time > self.attack_cooldown + self.weapon_cooldown:
                self.attacking = False
                self.destroy_weapon()
            if self.weapon_switch_time is not None:
                if current_time - self.weapon_switch_time > self.weapon_switch_cooldown:
                    self.can_switch_weapon = True

        if not self.vulnerable:
            if current_time - self.hurt_time > self.invincibility_duration:
                self.vulnerable = True
    
    def get_full_weapon_damage(self):
        if self.weapon:
            self.damage = self.stats['attack'] + weapon_data[self.weapon]['damage']
            print(f'Damage:{self.damage}')
            return self.damage
        else:
            pass
            # magic damage

    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldown()
        self.animate()
        ui(self.health,self.weapon,self.energy)


