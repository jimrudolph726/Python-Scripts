# weapon_data = {
#     'sword':{'cooldown': 100, 'damage': 15, 'graphic':'C:/Users/jimru/Desktop/Wyndmere_graphics/graphics/weapons/sword/full.png'},
#     'lance':{'cooldown': 400, 'damage': 30, 'graphic':'C:/Users/jimru/Desktop/Wyndmere_graphics/graphics/weapons/lance/full.png'},
#     'axe':{'cooldown': 300, 'damage': 20, 'graphic':'C:/Users/jimru/Desktop/Wyndmere_graphics/graphics/weapons/axe/full.png'},
#     'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'C:/Users/jimru/Desktop/Wyndmere_graphics/graphics/weapons/rapier/full.png'},
#     'sai':{'cooldown': 80, 'damage': 10, 'graphic':'C:/Users/jimru/Desktop/Wyndmere_graphics/graphics/weapons/sai/full.png'},
#   }

# print(weapon_data['sword']['cooldown'])

# x={'cooldown': 100, 'damage': 15, 'graphic':'C:/Users/jimru/Desktop/Wyndmere_graphics/graphics/weapons/sword/full.png'}
# print(x['cooldown'])
from random import choice
from support import import_folder
import pygame

frames = {
        # magic
        'flame': import_folder('../graphics/particles/flame/frames'),
        'aura': import_folder('../graphics/particles/aura'),
        'heal': import_folder('../graphics/particles/heal/frames'),
        
        # attacks 
        'claw': import_folder('../graphics/particles/claw'),
        'slash': import_folder('../graphics/particles/slash'),
        'sparkle': import_folder('../graphics/particles/sparkle'),
        'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
        'thunder': import_folder('../graphics/particles/thunder'),

        # monster deaths
        'squid': import_folder('../graphics/particles/smoke_orange'),
        'raccoon': import_folder('../graphics/particles/raccoon'),
        'spirit': import_folder('../graphics/particles/nova'),
        'bamboo': import_folder('../graphics/particles/bamboo'),
        
        # leafs 
        'leaf': (
            import_folder('../graphics/particles/leaf1'),
            import_folder('../graphics/particles/leaf2'),
            import_folder('../graphics/particles/leaf3'),
            import_folder('../graphics/particles/leaf4'),
            import_folder('../graphics/particles/leaf5'),
            import_folder('../graphics/particles/leaf6'),
            )
        }
animation_frames = choice(frames['leaf'])
frame_index = 0

frames = animation_frames
print(frames[0])
# image = frames[frame_index]
# 
# animation_speed = 0.15
# frames = animation_frames
# 
# print(image)
