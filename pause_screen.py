import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class PauseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )  # Added pygame.SRCALPHA to make the surface transparent
        self.overlay.fill((0, 0, 0, 128))  # Fill the overlay with a transparent color
        self.font = pygame.font.Font(None, 72)
        self.text = self.font.render("Paused", True, WHITE)
        self.text_rect = self.text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )

    def draw(self):
        # Draw the transparent overlay
        # self.screen.blit(self.overlay, (0, 0))

        # Draw the pause text
        self.screen.blit(self.text, self.text_rect)
