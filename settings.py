class Settings:

    # screen settings 
    def __init__(self):
        ''' Initializes the game's static settings. '''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 33, 1)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3 # width of 3 pixels
        self.bullet_height = 15 # height of 15 pixels
        self.bullet_color = (245, 245, 245)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10
      
        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        ''' Initialize settings that change throughout the game. '''
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction: 1 == right while -1 == Left.
        self.fleet_direction = 1

        # Scoring
        self.aliens_points = 50

    def increase_speed(self):
        ''' Increase speed settings & alien points. '''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.aliens_points = int(self.aliens_points * self.score_scale)