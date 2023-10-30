import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import TileMap

RENDER_SCALE = 2.0

# Creating level editor
class Editor:

    def __init__(self):

        # Initializing pygame
        pygame.init()

        # Setting title of game window
        pygame.display.set_caption('Level Editor')

        # Creates the window - Tuple is resolution in pixels
        self.screen = pygame.display.set_mode((640, 480))

        # Initializing a second display for rendering
        # Resolution is halved so that when scaled to window
        # Creates a pixel effect
        self.display = pygame.Surface((320, 240))

        # Initializing clock 
        self.clock = pygame.time.Clock()

        # Initializing assets/images
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
        }

        # Initializing movement for camera
        self.movement = [False, False, False, False]

        # Initializing tile map
        self.tilemap = TileMap(self)

        # Initializing 'camera' effect
        self.scroll = [0, 0]

        # Initializing list of tiles to place in editor
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Initializing variables for mouse buttons
        self.clicking = False
        self.right_clicking = False
        self.shift = False

    def run(self):

        # Creating game loop - each frame is an iteration in a loop
        while True:

            # Clearing screen every iteration
            self.display.fill((0, 0, 0))

            # Initiating offset
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Rendering tilemap
            self.tilemap.render(self.display, offset=render_scroll)

            # Displaying what tile we are currently using
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            self.display.blit(current_tile_img, (5, 5))

            # Getting coordinates of mouse pointer
            # Scaling down in terms of display rendering
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))

            # Placing/deleting tiles on editor
            if self.clicking == True:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type' : self.tile_list[self.tile_group], 'variant' : self.tile_variant, 'pos' : tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

            # Grabs user input
            for event in pygame.event.get():

                # Closing pygame + window
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

                # Creating mouse input for selecting and placing tiles
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                
                # Updating clicking variable based on mouse state
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                        

                # Camera movement input + Shift input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                
            # Scaling display to the size of the screen/window
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Updates display
            pygame.display.update()

            # Maintains 60 FPS
            self.clock.tick(60)

Editor().run()
