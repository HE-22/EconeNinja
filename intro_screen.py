import pygame
import sys


class IntroScreen:
    def __init__(self, screen_width, screen_height):
        """
        - Initialize the IntroScreen class.
        - Args: screen_width (int): width of the screen, screen_height (int): height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 36)
        self.play_button = pygame.Rect(
            self.screen_width / 2 - 50, self.screen_height / 2, 100, 50
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
        pygame.draw.rect(surface, (0, 255, 0), self.play_button)
        self.draw_text(
            "Play", surface, self.play_button.centerx, self.play_button.centery
        )

    def check_play_button(self, event):
        """
        - Check if the play button is clicked.
        - Args: event (pygame.Event): event to check
        - Returns: bool: True if the play button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
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

            self.screen.fill((0, 0, 0))
            self.draw_text(
                "Welcome to the Game",
                self.screen,
                self.screen_width / 2,
                self.screen_height / 4,
            )
            self.draw_button(self.screen)
            pygame.display.update()
