import pygame
from projectile import Projectile
import math
import random


class ProjectileShooter:
    def __init__(self, screen_width, screen_height, projectile_count=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active_projectiles = []
        self.inactive_projectiles = []
        self.shooting = True
        self.shoot_counter = 0  # Initialize shoot counter
        self.shoot_limit = 10  # Set shoot limit
        for _ in range(projectile_count):
            projectile = Projectile(
                screen_width, screen_height, math.pi
            )  # Set initial angle
            self.active_projectiles.append(projectile)

    def add_projectiles(self, count, angle):
        for _ in range(count):
            if self.inactive_projectiles:
                projectile = self.inactive_projectiles.pop()
                projectile.reset(
                    self.screen_width, self.screen_height, angle
                )  # Provide screen_width, screen_height, and initial angle
            else:
                projectile = Projectile(
                    self.screen_width, self.screen_height, angle
                )  # Set initial angle
            self.active_projectiles.append(projectile)
            self.shoot_counter += 1  # Increment shoot counter
            if self.shoot_counter >= self.shoot_limit:
                self.shooting = False  # Stop shooting when limit is reached
                self.shoot_counter = 0  # Reset shoot counter

    def increase_difficulty(self):
        for projectile in self.active_projectiles:
            projectile.speed += 0.1  # Increase speed by a smaller amount
        if self.active_projectiles:
            current_angle = self.active_projectiles[0].angle
            self.add_projectiles(1, current_angle)

    def move_projectiles(self):
        screen_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        new_active_projectiles = []
        for projectile in self.active_projectiles:
            projectile.move()
            if screen_rect.colliderect(projectile.rect):
                new_active_projectiles.append(projectile)
            else:
                self.inactive_projectiles.append(projectile)
        self.active_projectiles = new_active_projectiles

    def draw_projectiles(self, screen):
        for projectile in self.active_projectiles:
            projectile.draw(screen)
            pygame.draw.rect(screen, (255, 0, 0), projectile.rect, 2)  # Add this line

    def set_projectiles_direction(self, direction: str):
        """
        Set the direction of all active projectiles based on the given direction.
        Args:
            direction (str): The direction for the projectiles. It can be 'top', 'bottom', 'left', 'right'.
        """
        if direction == "top":
            angle = 0
        elif direction == "bottom":
            angle = math.pi
        elif direction == "left":
            angle = 3 * math.pi / 2
        elif direction == "right":
            angle = math.pi / 2
        else:
            raise ValueError(
                "Invalid direction. It can be 'top', 'bottom', 'left', 'right'."
            )

        for projectile in self.active_projectiles:
            projectile.angle = angle

    def switch_direction_after_all_projectiles_pass(self):
        """
        Wait for all the current projectiles to pass, then switch to a random direction.
        """
        if not self.active_projectiles:
            directions = {
                "top": 0,
                "bottom": math.pi,
                "left": 3 * math.pi / 2,
                "right": math.pi / 2,
            }
            new_direction = random.choice(list(directions.keys()))
            new_angle = directions[new_direction]
            self.set_projectiles_direction(new_direction)
            self.add_projectiles(self.shoot_limit, new_angle)
            self.shooting = True

    def update(self, screen):
        if self.shooting:
            self.move_projectiles()
            self.draw_projectiles(screen)
        else:
            self.switch_direction_after_all_projectiles_pass()

    def reset(self):
        self.active_projectiles.clear()
        self.inactive_projectiles.clear()
        for _ in range(5):
            projectile = Projectile(self.screen_width, self.screen_height, math.pi)
            self.active_projectiles.append(projectile)


