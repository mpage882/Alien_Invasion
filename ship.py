import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    # initialize the ship and starting positions
    # get_rect() is from pygame
    
    def __init__(self, ai_game):
        # pulling from Settings class and a_i class
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Loads image and gets its rectangles 
        self.image = pygame.image.load('images/ship_50.bmp')
        self.rect = self.image.get_rect()

        # starts each ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False


    # Update the ship's position based on the movement flag
    def update(self):

        # second part of if statement below  ('and ...') keeps ship from going off screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # update the ship's x value, not the rect
            # self.rect.x += 1
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    # draws the ship at its current location
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        ''' center ship on the screen '''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

