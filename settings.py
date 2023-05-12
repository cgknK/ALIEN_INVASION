import pygame

class Settings:
    """Oyunun ayarlarını store-saklayan- sınıf"""
    def __init__(self):
        bg_colors = {
            'grey' : (230, 230, 230),
            'blue' : (40, 160, 200),
            }

        resulutions = [ (800, 600), (500, 500)]

        image_paths = {
            'ship' : 'images/ship.bmp',
            'figure' : 'images/figure.bmp',
            }

        self.screen_width = resulutions[0][0]
        self.screen_height = resulutions[0][1]
        self.value_current_window = "Alien Invasion"
        self.bg_color = bg_colors['blue']
        self.image_path = image_paths['ship']
