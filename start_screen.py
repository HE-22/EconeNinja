import pygame
import sys
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class StartScreen:
    def __init__(self):
        """
        - Initialize the IntroScreen class.
        - Args: screen_width (int): width of the screen, screen_height (int): height of the screen
        """
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/fonts/PixeloidSansBold.ttf",
            36,
        )
        self.play_button = pygame.image.load(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/buttons/play_button.png"
        )
        self.play_button = pygame.transform.scale(self.play_button, (100, 50))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.center = (
            int(self.screen_width / 2 + 5),
            int(self.screen_height / 2 + 250),
        )
        self.player_idle_sprites = [
            pygame.image.load(
                f"/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/01-Idle/MN_NINJA_Idle_00{i}.png"
            )
            for i in range(10)
        ]
        self.player_idle_sprites = [
            pygame.transform.scale(sprite, (240, 240))  # Double the size of the sprite
            for sprite in self.player_idle_sprites
        ]
        self.current_sprite = 0
        self.sprite_update_time = pygame.time.get_ticks()
        self.background_image = pygame.image.load(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/map/start_screen.png"
        )
        self.background_image = pygame.transform.scale(
            self.background_image, (self.screen_width, self.screen_height)
        )

    def draw_text(self, text, surface, x, y):
        """
        - Draw text on a given surface.
        - Args: text (str): text to be drawn, surface (pygame.Surface): surface to draw on, x (int): x-coordinate, y (int): y-coordinate
        """
        text_obj = self.font.render(text, 1, (255, 255, 255))
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)

    def draw_button(self, surface):
        """
        - Draw the play button.
        - Args: surface (pygame.Surface): surface to draw on
        """
        surface.blit(self.play_button, self.play_button_rect.topleft)

    def check_play_button(self, event):
        """
        - Check if the play button is clicked.
        - Args: event (pygame.Event): event to check
        - Returns: bool: True if the play button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(event.pos):
                print("Play button clicked!")
                return True
        return False

    def run(self):
        """
        - Run the intro screen.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.check_play_button(event):
                    return

            self.screen.blit(self.background_image, (0, 0))
            self.draw_text(
                "EconeNinja",
                self.screen,
                self.screen_width / 2,
                (self.screen_height / 4) - 100,
            )
            self.draw_button(self.screen)
            if (
                pygame.time.get_ticks() - self.sprite_update_time > 200
            ):  # Slow down the frame rate
                self.current_sprite = (self.current_sprite + 1) % len(
                    self.player_idle_sprites
                )
                self.sprite_update_time = pygame.time.get_ticks()
            self.screen.blit(
                self.player_idle_sprites[int(self.current_sprite)],
                (
                    self.screen_width / 2 - self.screen_width * 0.1 + 10,
                    self.screen_height / 2 - 10,
                ),
            )
            pygame.display.update()
