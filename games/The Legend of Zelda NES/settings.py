# game setup
WIDTH    = 1024	
HEIGHT   = 500
FPS      = 60
TILESIZE = 64

weapon_data = {'sword': {'damage': 500, 'weapon_cooldown': 400},
               'lance': {'damage': 50, 'weapon_cooldown': 1000}}

enemy_data = {'red_darknut': {'health': 100, 'exp': 75, 'damage': 15, 'attack_type': 'slash', 
                              'attack_sound':'sound/sword.mp3', 'speed':3, 'resistance':3, 
                              'attack_radius': 80, 'notice_radius': 150},
              'blue_moblin': {'health': 80, 'exp': 55, 'damage': 10, 'attack_type': 'slash', 
                              'attack_sound':'sound/sword.mp3', 'speed':2.5, 'resistance':3, 
                              'attack_radius': 80, 'notice_radius': 150}}