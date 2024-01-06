import pygame
from projectile import Projectile
import math
import random


class ProjectileShooter:
    def __init__(self, screen_width, screen_height, projectile_count=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active_projectiles = []
        self.is_shooting = True
        for _ in range(projectile_count):
            projectile = Projectile(screen_width, screen_height, math.pi)
            self.active_projectiles.append(projectile)

    def switch_direction(self):
        directions = {
            "top": 0,
            "bottom": math.pi,
            "left": 3 * math.pi / 2,
            "right": math.pi / 2,
        }
        new_direction = random.choice(list(directions.values()))
        for projectile in self.active_projectiles:
            projectile.angle = new_direction

    def update(self, screen):
        if self.is_shooting:
            for projectile in self.active_projectiles:
                projectile.move()
                # Check if the projectile has moved off the screen
                if not (
                    0 <= projectile.x <= self.screen_width
                    and 0 <= projectile.y <= self.screen_height
                ):
                    # Reset the projectile
                    projectile.reset(self.screen_width, self.screen_height)
                else:
                    projectile.draw(screen)
