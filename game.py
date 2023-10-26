import sys

import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity #Importing player object
from scripts.tilemap import TileMap

class Game:

    def __init__(self):

        # Initializing pygame
        pygame.init()

        # Creates the window - Tuple for Resolution in pixels
        pygame.display.set_caption('Ninja Game')

        # Initializing display to be blit on screen (for pixel look)
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        # Initializing clock 
        self.clock = pygame.time.Clock()

        # Initializing movement variable
        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player' : load_image('entities/player.png')
        }


        # Initializing player entity
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = TileMap(self)

    def run(self):

        # Creating game loop - each frame is an iteration in a loop
        while True:
            self.display.fill((14, 219, 248))

            self.tilemap.render(self.display)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get(): #get() grabs user input
                if event.type == pygame.QUIT: #Window closed
                    pygame.quit() 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                
            #Scaling display to the size of the screen/window
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()

            self.clock.tick(60)

Game().run()
