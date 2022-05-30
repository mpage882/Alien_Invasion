import sys

from time import sleep   # creates pause in game

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
            self._update_aliens() 
            self._update_screen()

    def _check_fleet_edges(self):
        ''' Respond appropriately if any aliens have reached an edge '''
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        ''' Drop the entire fleet and change its direction '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        ''' Check if fleet is at an edge, then update the position of all aliens in fleet '''
        self._check_fleet_edges()

        ''' Updates positions of all aliens in fleet '''
        self.aliens.update()

        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!") # replace to test


    def _create_fleet(self):
        ''' Create the fleet from alien - spacing between alien = 1 alien width'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)  # floor division

        ''' Determine the number of rows of aliens that fit on the screen '''
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (7 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create 1st row of aliens by creating an alien and placing it in row
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_bullets(self):
        # Updates bullets position 
        self.bullets.update()   
        # deletes old ones
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens
        # if so, get rid of both alien and bullet
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        # Destroy existing bullets and create new fleet.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
                

    def _check_events(self):
        # responds to keypresses and mouse events
        # helper method
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