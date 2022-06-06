class GameStats:
    ''' Track stats for Alien Invasion '''

    def __init__(self, ai_game):
        ''' Initialize stats '''
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactie state for Play button.
        self.game_active = False
        
        # High should never be reset. So will be initialize in __init__ instead of reset_stats
        self.high_score = 0

    def reset_stats(self):
        ''' Initialize stats that can change during the game '''
        self.ships_left = self.settings.ship_limit
        self.score = 0
