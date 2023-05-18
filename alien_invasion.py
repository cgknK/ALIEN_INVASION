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
            (self.settings.screen_width, self.settings.screen_height)
            )
        self.value_current_window = self.settings.value_current_window
        pygame.display.set_caption(self.value_current_window)

        # self.ship'i olması için self'in olması gerekiyor. self'in olması için
        #de self.ship'in olması gerekiyor. Python burada C++'daki member init'i
        #mi kullanıyor? -implictly olarak-
        #self.ship in en sonda mı olması gerekiyor?Çünkü Ship(AlienInvasion)?
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game."""

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """"Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # bu exit() c/c++ daki exit()-abort()- gibi mi?
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        """We can use elif blocks here because each event is 
        connected to only one key. If the player presses both keys 
        at once, two separate events will be detected. _Anlamadım
        Ama elifleri if yapncada aynı şekilde çalışıyor
        """
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Redraw the screen during each pass through the loop."""
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