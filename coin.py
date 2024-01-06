import random
import pygame


class Coin:
    def __init__(self, screen_width: int, screen_height: int):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

        # List of coin images
        chocolate = "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/collectable/chocolate.png"
        cone = "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/collectable/econe.png"
        self.coin_images = [chocolate, cone]

        # Select a random image from the list
        coin_image_path = random.choice(self.coin_images)

        # Load the image and convert it to alpha
        original_image = pygame.image.load(coin_image_path).convert_alpha()

        # Scale the image down to 11x11 if it's the chocolate image
        if coin_image_path == chocolate:
            self.image = pygame.transform.scale(original_image, (30, 30))
        else:
            self.image = original_image

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)  # Added this line

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
