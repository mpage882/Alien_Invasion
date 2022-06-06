import sys

from time import sleep   # creates pause in game

import pygame

from settings import Settings

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button

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
        
        self.stats = GameStats(self) # create instance to store game stats
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Makes the play button.
        self.play_button = Button(self, "Play")


    # starts main loop for game
    def run_game(self):
        while True:

            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens() 

            self._update_screen()


    def _check_aliens_bottom(self):
        ''' check to see if any alien has reached bottom of the of the screen '''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            ''' treated the same as collision '''
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _ship_hit(self):
        ''' responds to the ship being hit by alien. '''
        if self.stats.ships_left > 0:
            # decrement ships_left
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1.0)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(False)


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
            self._ship_hit() # print("Ship hit!!!") # replace to test
        
        # looks for aliens hitting the bottom
        self._check_aliens_bottom()


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
            self.settings.increase_speed()
                

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
            # play button event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


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
        # Try it yourself 14-1 Press P to Play
        elif event.key == pygame.K_p:
            self._start_game()


    def _check_keyup_events(self, event):
        # Makes movement stop when not pressing keys
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _start_game(self):
        # Try it yourself 14-1
        if not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True    

            # Gets rid of remaining aliens & bullets
            self.aliens.empty()
            self.bullets.empty()

            # Creates new fleet and ship
            self._create_fleet()
            self.ship.center_ship()   

            # Hides the cursor.
            pygame.mouse.set_visible(False)


    def _check_play_button(self, mouse_pos):
        ''' Starts a new game when the player clicks Play. '''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)  
        if button_clicked:
            self._start_game() 


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

        # Draws scoreboard on screen
        self.sb.show_score()

        # Draws the play button if game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # makes the most recently drawn screen visible
        pygame.display.flip()



if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()