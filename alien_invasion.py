import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """
    Overall class to manage game assets and behavior.
    """

    def __init__(self):
        """
        Initialize the game, and create game resources.
        """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # self.ship'i olması için self'in olması gerekiyor. self'in olması için
        #de self.ship'in olması gerekiyor. Python burada C++'daki member init'i
        #mi kullanıyor? -implictly olarak-
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # bu exit() c/c++ daki exit()-abort()- gibi mi?
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            #bu fill() methodu nereden geliyor?(pygame.display mı?)
            #sanki pygame.display.fill() olmalıymış gibi geliyor mantığı düzelt
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            # Make the most recently drawn screen visible.
            pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()