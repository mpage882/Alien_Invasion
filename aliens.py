import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    ''' A class to represent a single alien in fleet '''

    # Initializes alien and sets starting position
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Loading alien image
        self.image = pygame.image.load("images/alien_1.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left
        self.rect.x = self.rect.width # adds space to left of ship that equals to ship's width
        self.rect.y = self.rect.height # adds space above that equals height of ship

        # Store the alien's exact horiz. position which will be used to track speed
        self.x = float(self.rect.x)

    def update(self):
        ''' Move alien from left to right '''
        self.x += self.settings.alien_speed
        self.rect.x = self.x
