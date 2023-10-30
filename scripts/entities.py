import pygame

class PhysicsEntity:

    # Note: Parameter - 'game'
    # Anything accessible by the game is accessible by the entity
    # Used to directly reduce scope issues with interactions
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    # Creating collision hitbox for entity, Updated based on position
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    # Setting the animation currently being displayed by the entity
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    # Handling updates for entity movement, collisions, etc.
    def update(self, tilemap, movement=(0, 0)):

        # Keeps track of collisions we've had, resetting it each frame
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        # Creating a vector for how much entity should be moved in frame in relation to passed in movement
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Entity movement in two stages (x-axis)
        self.pos[0] += frame_movement[0]

        # Creating hitbox and handling collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        # Entity movement in two stages (y-axis)
        self.pos[1] += frame_movement[1]

        # Creating hitbox and handling collisions
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        #Flipping character when moving different directions
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Adding terminal velocity/gravity - 5 is our max velocity downwards
        # Modifying downward velocity by 0.1
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Resetting y-velocity if we hit the ground/ceiling
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    # Rendering the entity onto the screen
    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
        

#Writing animation logic for PLAYER which inherits Entity class
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')