import pygame

class Ship:
    """Gemiyi yöneten sınıf"""
    def __init__(self, ai_game):
        """Gemiyi başlat ve başlangıç konumunu belirle."""
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

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    """The update() method will be called through an instance of Ship, so
    it’s not considered a helper method. _Anlamadım
    """
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Gemiyi mevcut konuma çiz"""
        self.screen.blit(self.image, self.rect)

