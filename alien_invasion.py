import sys

import pygame

from settings import Settings

from ship import Ship 

from bullets import Bullets

from aliens import Alien


class AlienInvasion:
# manages all of the game

    # initialize the game and create resources
    def __init__(self):
        pygame.init()

        self.settings = Settings()

        # NOTE: Maybe I can make an if/else statement to allow screen size changes
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


    # starts main loop for game
    def run_game(self):
        while True:

            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            
    def _create_fleet(self):
        ''' Create the fleet from alien'''
        alien = Alien(self)
        self.aliens.add(alien)


    def _update_bullets(self):
        # Updates bullets position 
        self.bullets.update()   
        # deletes old ones
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                

    # responds to keypresses and mouse events
    # helper method
    def _check_events(self):
        # watches for events (keyboard and mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True     
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        # Makes movement stop when not pressing keys
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                

    def _fire_bullet(self):
        ''' Create a new bullet and add it to the bullets group. '''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)


    # updates images on screen and flip  to new screen
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)  
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.aliens.draw(self.screen)

        # makes the most recently drawn screen visible
        pygame.display.flip()



if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()