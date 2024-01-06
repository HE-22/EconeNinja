import pygame
from projectile import Projectile
import math


class ProjectileShooter:
    def __init__(self, screen_width: int, screen_height: int, projectile_count=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active_projectiles = []
        self.current_direction = math.pi  # Default direction to the left
        self.projectile_count = projectile_count

        for _ in range(projectile_count):
            self.spawn_projectile()

    def spawn_projectile(self):
        """
        Spawns a new projectile in the current direction.
        """
        projectile = Projectile(
            self.screen_width, self.screen_height, self.current_direction
        )
        self.active_projectiles.append(projectile)

    def set_direction(self, direction: float):
        """
        Sets a new direction for all existing and future projectiles.
        """
        self.current_direction = direction
        for projectile in self.active_projectiles:
            projectile.set_direction(self.current_direction)

    def update(self, screen: pygame.Surface):
        """
        Updates and draws active projectiles.
        """
        for projectile in self.active_projectiles:
            projectile.move()
            if not (
                0 <= projectile.x <= self.screen_width
                and 0 <= projectile.y <= self.screen_height
            ):
                self.active_projectiles.remove(projectile)
                self.spawn_projectile()  # Keep the number of projectiles consistent
            else:
                projectile.draw(screen)
    def reset(self):
        """
        Resets the state of the ProjectileShooter.
        """
        self.active_projectiles = []
        for _ in range(self.projectile_count):
            self.spawn_projectile()
