import pygame
# Bu zaten pygame içinde değil mi? Bunu importlamaz isek neden hata veriyor?
from pygame.sprite import Sprite

class Ship(Sprite):
    """Gemiyi yöneten sınıf"""
    def __init__(self, ai_game):
        """Gemiyi başlat ve başlangıç konumunu belirle."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image_value = ai_game.settings.image_path
        self.image = pygame.image.load(self.image_value)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_right, self.moving_left = False, False
        self.moving_up = False
        self.moving_down = False

        self.count = 0

    """The update() method will be called through an instance of Ship, so
    it’s not considered a helper method. _Anlamadım
    """
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right:
            if self.rect.left < self.screen_rect.right:
                self.x += self.settings.ship_speed_x
            else:
                self. x = self.screen_rect.left
        if self.moving_left:
            if self.rect.right > 0:
                self.x -= self.settings.ship_speed_x
            else:
                self.x = self.screen_rect.right

        # Update the ship's y value, not the rect.
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed_y
        # Burada ilişkisel operatörde neden <= kullanılmış, görünürde hiç bir
        #şey değişmiyor?
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed_y
        
        # Update rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Gemiyi mevcut konuma çiz"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)