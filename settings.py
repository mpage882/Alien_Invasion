class Settings:

    # screen settings 
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 33, 1)

        # ship settings
        self.ship_speed = 1.5

        # bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3 # width of 3 pixels
        self.bullet_height = 15 # height of 15 pixels
        self.bullet_color = (245, 245, 245)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0 # was 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 == right while -1 == Left

        