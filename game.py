import sys
import pygame

class Game:

    def __init__(self):

        # Initializing pygame
        pygame.init()

        # Creates the window - Tuple for Resolution in pixels
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Ninja Game')

        # Initializing clock object
        self.clock = pygame.time.Clock()

        # Initializing cloud image
        self.img = pygame.image.load('data/images/clouds/cloud_1.png')

    def run(self):
        # Creating game loop - each frame is an iteration in a loop
        while True:
            self.screen.blit(self.img, (100, 200))
            
            for event in pygame.event.get(): #Get grabs user input
                if event.type == pygame.QUIT: #Window closed
                    pygame.quit() 
                    sys.exit()
            
            # Updates display
            pygame.display.update()
            self.clock.tick(60) #60 FPS, clock sleeps for _ to maintain FPS

Game().run()
