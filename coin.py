import random
import pygame


class Coin:
    def __init__(self, screen_width: int, screen_height: int):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.image = pygame.image.load(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/collectable/econe.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)  # Added this line

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
