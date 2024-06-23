import pygame, sys
from settings import *
from  level import Level
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

class Game:
    def __init__(self):
        pygame.init()

        # Load the MP3 file for overworld music
        pygame.mixer.music.load(fr'C:\Users\jimru\Documents\GitHub\Python-Scripts\games\The Legend of Zelda NES\sound\overworld.mp3')
        # Play the MP3 file in an infinite loop
        pygame.mixer.music.play(-1)
  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
   
        self.level=Level()
    
    def run(self): 
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.run()
            self.clock.tick(FPS)
            pygame.display.update()

if __name__ == '__main__':
    game=Game()
    game.run()