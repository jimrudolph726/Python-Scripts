import pygame
pygame.init()
font = pygame.font.Font(None,30)

def ui(health,weapon,energy):
    display_surface = pygame.display.get_surface()

    # health bar display
    health_bar_background = pygame.Rect(28, 23, 105, 17)
    pygame.draw.rect(display_surface,'Black',health_bar_background)
    health_bar = pygame.Rect(30, 25, health, 10)
    pygame.draw.rect(display_surface,'Red',health_bar)
    
    # health text display
    health_text_background = pygame.Rect(30, 0, 65, 20)
    pygame.draw.rect(display_surface,'Black',health_text_background)
    health_text = font.render(str('health'),True,'White')
    display_surface.blit(health_text,(30,0))

    # energy bar display
    energy_bar_background = pygame.Rect(138, 23, 105, 17)
    pygame.draw.rect(display_surface,'Black',energy_bar_background)
    energy_bar = pygame.Rect(140, 25, energy, 10)
    pygame.draw.rect(display_surface,'Blue',energy_bar)
    
    # energy text display
    energy_text_background = pygame.Rect(140, 0, 65, 20)
    pygame.draw.rect(display_surface,'Black',energy_text_background)
    energy_text = font.render(str('energy'),True,'White')
    display_surface.blit(energy_text,(140,0))

    # current weapon display
    weapon_background = pygame.Rect(258, 5, 64, 64)
    pygame.draw.rect(display_surface,'Black',weapon_background)
    weapon_image = pygame.image.load(fr'C:\Users\jimru\Desktop\zelda_nes\graphics\weapons\{weapon}\up.png').convert_alpha()
    weapon_rect = weapon_image.get_rect(midtop = (290,5))
    display_surface.blit(weapon_image,weapon_rect)