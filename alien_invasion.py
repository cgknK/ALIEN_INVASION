import sys
import pygame

class AlienInvasion:
    """
    Overall class to manage game assets and behavior.
    """

    def __init__(self):
        """
        Initialize the game, and create game resources.
        """

        pygame.init()

        # neden set_mode iki parantezler yazılmış?
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
        # Set the background color.
        self.bg_color = (230, 230, 230)

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
            self.screen.fill(self.bg_color)
            # Make the most recently drawn screen visible.
            pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()