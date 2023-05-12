import pygame

class Ship:
    """Gemiyi yönetecek sınıf"""
    def __init__(self, ai_game):
        """Gemiyi başlat ve başlangıç konumunu belirle."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image_value = ai_game.settings.image_path
        self.image = pygame.image.load(self.image_value)
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Gemiyi mevcut konuma çiz"""
        self.screen.blit(self.image, self.rect)

