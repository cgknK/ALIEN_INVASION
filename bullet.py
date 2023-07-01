import pygame
# Zaten tüm pygame import edilmemiş mi, Sprite'da bunun içinde değil mi?
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Create a bullet object at the ship's current position."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    """
    def __del__(self):
        print(self)
    """

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed

        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class AlienBullet(Sprite):
    """Create a bullet object at the ship's current position."""
    def __init__(self, ai_game, alien_this):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color_alien

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                            self.settings.bullet_height*7.5)
        self.rect.midtop = alien_this.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y += 0.5

        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

# isim anlamsız değiştirilecek, refactoring yapılacak
class BulletMulti(Sprite):
    """Create a bullet object at the ship's current position."""
    def __init__(self, ai_game, mTip, yan):
        super().__init__()
        self.mermiTip = mTip
        self.yan = yan
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    """
    def __del__(self):
        print(self)
    """

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        if self.mermiTip == -1:
            self.x += self.settings.bullet_speed * 0.1
            if self.yan == 1:
                self.x += self.settings.bullet_speed
                self.y += self.settings.bullet_speed
        elif self.mermiTip == 0:
            pass
        elif self.mermiTip == 1:
            self.x -= self.settings.bullet_speed * 0.1
            if self.yan == 1:
                self.x -= self.settings.bullet_speed
                self.y += self.settings.bullet_speed

        # Update the rect position.
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
