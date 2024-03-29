import sys
from time import sleep
import json
from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet, AlienBullet, BulletMulti
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()
        if self.settings.screen_width == 0 or self.settings.screen_height == 0:
            self.screen = pygame.display.set_mode((0,0),(pygame.FULLSCREEN))
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                    (self.settings.screen_width, self.settings.screen_height))

        self.value_current_window = self.settings.value_current_window
        pygame.display.set_caption(self.value_current_window)

        # Create an instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # self.ship'i olması için self'in olması gerekiyor. self'in olması için
        #de self.ship'in olması gerekiyor. Python burada C++'daki member init'i
        #mi kullanıyor? -implictly olarak-
        #self.ship in en sonda mı olması gerekiyor?Çünkü Ship(AlienInvasion)?
        self.ship_sprite_group = pygame.sprite.Group()
        self.ship = Ship(self)
        self.ship_sprite_group.add(self.ship)

        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #  Make the Play button.
        self.play_button = Button(self, "Play", 0)

        # Make difficulty buttons.
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Make buttons that allow player to select difficulty level."""
        # Make the Easy_Level button.-default-
        self.easy_button = Button(self, "Easy Level", 1)
        # Make the Hard_Level button.
        self.hard_button = Button(self, "Hard Level", 2)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien_bullets()
                self._update_aliens()
                
            self._update_screen()

    def _check_events(self):
        """"Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._save_and_exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
        elif hard_button_clicked:
            self.settings.difficulty_level = 'hard'

    def _start_game(self):
        """Start a new game."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

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
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self._save_and_exit()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_h:
            self.settings.difficulty_level = 'hard'
        elif event.key == pygame.K_e:
            self.settings.difficulty_level = 'easy'
        #print("event.key",event.key)#event.key 27 -> esc

    def _save_and_exit(self):
        """Save high score and exit."""

        # Her zaman dosya yazma maliyetinden kaçınmak için if kullanılabilinir
        #try:
        with open('high_score.json', 'w') as f:
            json.dump(self.stats.high_score, f)
        # Tüm exceptler nasıl yakalanır?
        #except:

        # bu exit() c/c++ daki exit()-abort()- gibi mi?
        sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    #refaktor
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            #new_bullet = Bullet(self)
            new_bullet = BulletMulti(self,-1,0)
            self.bullets.add(new_bullet)
            new_bullet = BulletMulti(self,0,0)
            self.bullets.add(new_bullet)
            new_bullet = BulletMulti(self,1,0)
            self.bullets.add(new_bullet)
            new_bullet = BulletMulti(self,-1,1)
            self.bullets.add(new_bullet)
            new_bullet = BulletMulti(self,1,1)
            self.bullets.add(new_bullet)
        #settings.bullets_allowed = 0 ise hiç mermi atamaz
        #settings.bullets_allowed = 0.5 bile olsa sınırsız
        #settings.bullets_allowed limitlemesi çalışmıyor, düzeltilecek.
        #print("total_fire_bullet", len(self.bullets))

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        # When you use a for loop with a list (or a group in Pygame), 
        #Python expects that the list will stay the same length as long as 
        #the loop is running.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                # Buradaki remove destucre'ı nasıl çağırıyor?
                self.bullets.remove(bullet)
                #print("update1", len(self.bullets))
            #update2 'ye hiç girmiyor
            onerme1 = bullet.rect.left >= self.screen.get_rect().right
            onerme2 = bullet.rect.right <= self.screen.get_rect().left
            if onerme1 or onerme2:
                # Buradaki remove destucre'ı nasıl çağırıyor?
                self.bullets.remove(bullet)
                #print("update2", len(self.bullets))

        """
        If you leave it in, the game will slow down significantly because 
        it takes more time to write output to the terminal than it does to 
        draw graphics to the game window.
        _Neden terminale birşey yazdırmak daha çok zaman alıyor?
        """
        print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # En son False'ı True yap
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            # Şunu test koduna ekle, nasıl olacaksa!!!
            #print(self.stats.score)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()
            # increase_speed() _create_fleet()'in altında olmasına rağmen
            #nasıl çoktan örneği oluşturulmuş nesnelere etki ediyor?
            #Anladım ama yinede yukarısında tanımlanması daha mantıklı değil mi?
            #self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, 
            then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # Biraz esneme payı verilebilir
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.

        # Bu alien destructure çağrılıyor mu? yani yok ediliyor mu? Evet.
        alien = Alien(self)
        alien.no = -1
        alien_width, alien_height = alien.rect.size

        # Bu degiskenler eğer çok ağır hesaplamalar içerseydi self.degiskenler
        #yapıp 1 kere hesaplanması sağlanır mıydı?
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            # Create the first row of aliens.
            for alien_number in range(number_aliens_x):
                # Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        random_number = randint(0, 15)
        if random_number == alien_number * row_number:
            alien.is_active = True
            # bu if anlamsız, neden koymuşum
            if len(self.bullets) < 1:
                new_bullet = AlienBullet(self, alien)
                self.alien_bullets.add(new_bullet)
        self.aliens.add(alien)

    def _update_alien_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.alien_bullets.update()

        screen_rect = self.screen.get_rect()
        # Get rid of bullets that have disappeared.
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= screen_rect.bottom:
                # Buradaki remove destucre'ı nasıl çağırıyor?
                self.alien_bullets.remove(bullet)

        #1_000_000, 999_983 veya ihtimalin yanına min bekleme süresi
        random_number = randint(0, 1_000_000)
        for alien in self.aliens.sprites():
            if alien.is_active and random_number >= 999_000:#999_909:
                if len(self.alien_bullets) < 1:
                    new_bullet = AlienBullet(self, alien)
                    self.alien_bullets.add(new_bullet)

        self._check_bullet_ship_collisions()

    def _check_bullet_ship_collisions(self):
        collisions = pygame.sprite.groupcollide(
                self.ship_sprite_group, self.alien_bullets, True, True)

        if collisions:
            for aliens in collisions.values():
                self._ship_hit()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Redraw the screen during each pass through the loop."""
        #bu fill() methodu nereden geliyor?(pygame.display mı?)
        #sanki pygame.display.fill() olmalıymış gibi geliyor mantığı düzelt
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self._draw_buttons()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _draw_buttons(self):
        self.play_button.draw_button()
        self.easy_button.draw_button()
        self.hard_button.draw_button()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()