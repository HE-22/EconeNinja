import pygame
import random
import math


class Projectile:
    def __init__(self, screen_width: int, screen_height: int, angle: float = math.pi):
        self.x = screen_width  # Start projectiles from the right of the screen
        self.y = random.randint(0, screen_height)
        self.speed = random.randint(5, 10)  # Increase speed range
        self.angle = angle  # Make projectiles move to the left
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

        # Load a random shurikan image
        self.image = pygame.image.load(
            f"/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/projectiles/shurikan/{random.randint(1, 7)}.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(
            self.image
        )  # Create mask for pixel-perfect collision

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (int(self.x), int(self.y))
        print(f"Projectile moved to ({self.x}, {self.y})")

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def update_collision_mask(self):
        """
        Update the collision mask to match the current sprite.
        Call this method if the sprite image changes.
        """
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self, screen_width: int, screen_height: int):
        directions = {
            "top": math.pi,  # bottom
            "bottom": 0,  # top
            "left": math.pi / 2,  # right
            "right": 3 * math.pi / 2,  # left
        }
        self.angle = random.choice(list(directions.values()))
        if self.angle == math.pi:  # bottom
            self.x = random.randint(0, screen_width)
            self.y = 0
        elif self.angle == 0:  # top
            self.x = random.randint(0, screen_width)
            self.y = screen_height
        elif self.angle == math.pi / 2:  # right
            self.x = 0
            self.y = random.randint(0, screen_height)
        elif self.angle == 3 * math.pi / 2:  # left
            self.x = screen_width
            self.y = random.randint(0, screen_height)
        self.speed = random.randint(5, 10)  # Increase speed range
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

        print(
            f"Projectile reset at ({self.x}, {self.y}) with angle {self.angle}"
        )  # Add this line
