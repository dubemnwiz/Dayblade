import sys

import pygame

from scripts.entities import PhysicsEntity #Importing player object

class Game:

    def __init__(self):

        # Initializing pygame
        pygame.init()

        # Creates the window - Tuple for Resolution in pixels
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Ninja Game')

        # Initializing clock object
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50 , 300, 50)

        self.player = PhysicsEntity(self, 'player', (50,50), (8,15))

    def run(self):

        # Creating game loop - each frame is an iteration in a loop
        while True:
            self.screen.fill((14, 219, 248))
            
            self.player.update(self.movement[1]-self.movement[0], 0)
            self.player.render(self.screen)

            for event in pygame.event.get(): #get() grabs user input
                if event.type == pygame.QUIT: #Window closed
                    pygame.quit() 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                
            
            # Updates display
            pygame.display.update()
            self.clock.tick(60) #60 FPS, clock sleeps for _ to maintain FPS

Game().run()
