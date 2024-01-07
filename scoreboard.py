import pygame
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

GAME_FONT_PATH = config["game_font_path"]
SCOREBOARD_FONT_SIZE = config["scoreboard_font_size"]
SCREEN_WIDTH = config["screen"]["width"]
HEART_SPRITE_PATH = config["heart_sprite_path_2"]


class Scoreboard:
    def __init__(self, y):
        """
        - Initialize the Scoreboard.
        - Args: y (int): y position of the scoreboard
        """
        self.font = pygame.font.Font(GAME_FONT_PATH, SCOREBOARD_FONT_SIZE)
        self.score = 0
        self.hearts = 3
        self.y = y
        self.heart_image = pygame.image.load(HEART_SPRITE_PATH).convert_alpha()
        self.heart_image.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

    def draw(self, screen):
        """
        - Draw the scoreboard on the screen.
        - Args: screen (pygame.Surface): the screen to draw on
        """
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_x = SCREEN_WIDTH - score_text.get_width() - 10
        screen.blit(score_text, (score_x, self.y))

        for i in range(self.hearts):
            screen.blit(
                self.heart_image,
                (
                    SCREEN_WIDTH - (i + 2) * self.heart_image.get_width() - i * 10,
                    self.y + 30,
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
