import pygame
from config import (
    GAME_FONT_PATH,
    SCOREBOARD_FONT_SIZE,
    SCREEN_WIDTH,
    ECONE_SPRITE_PATH,
    PLAYER_LIVES,
    WHITE,
    RED,
    BLACK,
)


class Scoreboard:
    def __init__(self, y):
        """
        - Initialize the Scoreboard.
        - Args: y (int): y position of the scoreboard
        """
        self.font = pygame.font.Font(GAME_FONT_PATH, SCOREBOARD_FONT_SIZE)
        self.score = 0
        self.hearts = PLAYER_LIVES
        self.y = y
        original_heart_image = pygame.image.load(ECONE_SPRITE_PATH).convert_alpha()
        width, height = original_heart_image.get_size()
        self.heart_image = pygame.transform.scale(
            original_heart_image, (width * 2, height * 2)
        )  # Scale the image to 2x its original size while keeping aspect ratio
        self.heart_image.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

    def draw(self, screen):
        """
        - Draw the scoreboard on the screen.
        - Args: screen (pygame.Surface): the screen to draw on
        """
        score_text = self.font.render(f"{self.score}", True, BLACK)
        score_x = 10  # Changed this line
        screen.blit(score_text, (score_x, self.y))

        for i in range(self.hearts):
            screen.blit(
                self.heart_image,
                (
                    SCREEN_WIDTH
                    - (i + 1) * self.heart_image.get_width()
                    - 10,  # Changed this line
                    self.y - 8,  # adjusted 8 to even out the heart y pos with the score
                ),
            )

    def update_score(self, score):
        """
        - Update the score.
        - Args: score (int): the new score
        """
        self.score = score

    def update_hearts(self, hearts):
        """
        - Update the number of hearts.
        - Args: hearts (int): the new number of hearts
        """
        self.hearts = hearts
