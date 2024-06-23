import pygame
from settings import *
from entity import Entity
from support import import_graphics

class Enemy(Entity):
    def __init__(self,enemy_id,pos,groups,obstacle_sprites,damage_player,trigger_enemy_death):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.enemy_id = enemy_id
        if self.enemy_id == '15': enemy_name = 'red_darknut'
        if self.enemy_id == '3': enemy_name = 'blue_moblin'

        self.enemy_name = enemy_name
        self.attack_cooldown = 400
        self.attack_time = None
        self.health        = enemy_data[enemy_name]['health']
        self.exp           = enemy_data[enemy_name]['exp']
        self.damage        = enemy_data[enemy_name]['damage']
        self.attack_type   = enemy_data[enemy_name]['attack_type']
        self.attack_sound  = enemy_data[enemy_name]['attack_sound']
        self.speed         = enemy_data[enemy_name]['speed']
        self.resistance    = enemy_data[enemy_name]['resistance']
        self.attack_radius = enemy_data[enemy_name]['attack_radius']
        self.notice_radius = enemy_data[enemy_name]['notice_radius']
        self.attacking = False
        self.direction.x = 1
        self.direction.x = 0

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        
        # graphics setup
        self.import_enemy_graphics(enemy_name)
        self.status = 'idle'
        self.image = self.enemy_animations[self.status][self.frame_index]
        
        # movement
        self.pos = pos
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.trigger_enemy_death = trigger_enemy_death

    def import_enemy_graphics(self,enemy_name):
        animations_path = fr'C:\Users\jimru\Desktop\zelda_nes\graphics\enemies\{enemy_name}'
        self.enemy_animations = {'move':[],'idle':[],'attack':[]}
        for key in self.enemy_animations.keys():
            full_path = animations_path + '/' + str(key)
            self.enemy_animations[key] = import_graphics(full_path)

    def get_player_distance_and_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else: 
            direction = pygame.math.Vector2((0,0))

        return(distance, direction)

    def get_status(self,player):
        distance = self.get_player_distance_and_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack == True:
            self.status = 'attack'
            self.attack_time = pygame.time.get_ticks()
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self,player):
        if self.status == 'attack':
            self.damage_player(self.damage,self.attack_type)
            self.can_attack = False
            
        elif self.status == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2((0,0))

    def animate(self,player):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.enemy_animations[self.status]):
            if self.status == 'attack':
                self.can_attack = False

            self.frame_index = 0
        self.image = self.enemy_animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.can_attack == False:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time > self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            # self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                pass
                # magic damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_enemy_death(self.enemy_name,self.rect.center)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def enemy_update(self,player):
        self.hit_reaction()
        self.move(self.speed)
        self.get_status(player)
        self.actions(player)
        self.animate(player)
        self.cooldowns()
        self.check_death()