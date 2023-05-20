import pygame

class Settings:
    """Oyunun ayarlarını store-saklayan- sınıf"""
    def __init__(self):
        """Initialize the game's static settings."""
        bg_colors = {
            'grey' : (230, 230, 230),
            'blue' : (40, 160, 200),
            'white' : (250, 250, 250)
            }

        resulutions = [ (800, 600), (500, 500)]

        image_paths = {
            'ship' : 'images/ship.bmp',
            'figure' : 'images/figure.bmp',
            }

        # Screen settings
        self.screen_width = resulutions[0][0]
        self.screen_height = resulutions[0][1]
        self.value_current_window = "Alien Invasion"
        self.bg_color = bg_colors['grey']

        # Ship settings
        self.image_path = image_paths['ship']
        self.ship_limit = 3

        # Bullet settings
        self.bullets = [ [3, 15], [300, 15], [3000, 15] ]
        self.bullet_width, self.bullet_height = self.bullets[2]
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        """We include fleet_direction in this method so the aliens always move 
        right at the beginning of a new game. _Buraya dahil edilmeden de 
        sıfırlanmıyor mu? Yoksa yapmaya çalışılan başka birşey mi?
        """
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.difficulty_level = 'easy'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.difficulty_level == 'easy':
            self.ship_speed = 0.8
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.bullet_speed = 1.6
            self.alien_speed = 0.2
        elif self.difficulty_level == 'hard':
            self.ship_limit = 3
            self.bullets_allowed = 3
            self.ship_speed = 1.5
            self.bullet_speed = 2.5
            self.alien_speed = 0.5

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'hard':
            pass

        difficulty_level = diff_setting