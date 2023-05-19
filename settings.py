import pygame

class Settings:
    """Oyunun ayarlarını store-saklayan- sınıf"""
    def __init__(self):
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

        self.screen_width = resulutions[0][0]
        self.screen_height = resulutions[0][1]
        self.value_current_window = "Alien Invasion"
        self.bg_color = bg_colors['grey']

        # Ship settings
        self.ship_speed = 1.5
        self.image_path = image_paths['ship']

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3