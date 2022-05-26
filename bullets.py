import pygame
from pygame.sprite import Sprite

class Bullets(Sprite):
    ''' Class to manage bullets from the ship '''

    def __init__(self, ai_game):
        ''' Creates bullet object at the ship's current location. '''

        super().__init__()
        # inherets from Sprite (groups related items in game)

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect at (0, 0) & then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        ''' moves the bullet up the screen '''
        self.y -= self.settings.bullet_speed # updates the decimal position of the bullet/increases speed as game progresses

        self.rect.y = self.y # updates the rect's position

    def draw_bullet(self):
        ''' Draw the bullet to the screen '''
        pygame.draw.rect(self.screen, self.color, self.rect)