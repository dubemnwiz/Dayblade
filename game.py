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

        # Initializing cloud image
        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0, 0, 0)) #Makes black background transparent

        self.img_pos = [160, 260]
        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50 , 300, 50)

        self.player = physicsEntity(self, 'player', (50,50), (8,15))
    def run(self):

        # Creating game loop - each frame is an iteration in a loop
        while True:
            self.screen.fill((14, 219, 248))
            
            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.screen.blit(self.img, self.img_pos) #Collage of diff images on screen (putting cloud on screen)c

            for event in pygame.event.get(): #get() grabs user input
                if event.type == pygame.QUIT: #Window closed
                    pygame.quit() 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                
            
            # Updates display
            pygame.display.update()
            self.clock.tick(60) #60 FPS, clock sleeps for _ to maintain FPS

Game().run()
