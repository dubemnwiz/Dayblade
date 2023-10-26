import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity #Importing entity object
from scripts.tilemap import TileMap
from scripts.clouds import Clouds

class Game:

    def __init__(self):

        # Initializing pygame
        pygame.init()

        # Setting title of game window
        pygame.display.set_caption('Ninja Game')

        # Creates the window - Tuple is resolution in pixels
        self.screen = pygame.display.set_mode((640, 480))

        # Initializing a second display for rendering
        # Resolution is halved so that when scaled to window
        # Creates a pixel effect
        self.display = pygame.Surface((320, 240))

        # Initializing clock 
        self.clock = pygame.time.Clock()

        # Initializing movement variable
        self.movement = [False, False]

        # Initializing assets/images
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds'),
        }

        # Initializing clouds
        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Initializing player entity
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        # Initializing tile map
        self.tilemap = TileMap(self)

        # Initializing 'camera' effect
        self.scroll = [0, 0]

    def run(self):

        # Creating game loop - each frame is an iteration in a loop
        while True:

            # Clearing screen every iteration
            self.display.blit(self.assets['background'], (0, 0))

            # Centering camera on player
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            
            # Creating int version of scroll to fix jittering of pixels
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Updating + Rendering clouds
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # Rendering tile map
            self.tilemap.render(self.display, offset=render_scroll)
            
            # Updating + Rendering player based on movement
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, render_scroll)

            # Grabs user input
            for event in pygame.event.get():

                # Closing pygame + window
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
                
                # Movement input
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
                
            # Scaling display to the size of the screen/window
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Updates display
            pygame.display.update()

            # Maintains 60 FPS
            self.clock.tick(60)

Game().run()
