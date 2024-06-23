import pygame
from settings import *

class Text:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()

    def display_text(self,player):
            if player.touch:
                # assigning values to X and Y variable
                X = 400
                Y = 400
                white = (255, 255, 255)
                green = (0, 255, 0)
                blue = (0, 0, 128)

                # create a font object.
                # 1st parameter is the font file
                # which is present in pygame.
                # 2nd parameter is size of the font
                font = pygame.font.Font('freesansbold.ttf', 30)
                
                # create a text surface object,
                # on which text is drawn on it.
                text = font.render('test', True, green, blue)
                
                # create a rectangular object for the
                # text surface object
                textRect = text.get_rect()
                
                # set the center of the rectangular object.
                textRect.center = (X // 2, Y // 2)
                
                # copying the text surface object
                # to the display surface object
                # at the center coordinate.
                # self.display_surface.blit(text, textRect)
                
            