import pygame
from projectile import Projectile


class ProjectileShooter:
    def __init__(self, screen_width, screen_height, projectile_count=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active_projectiles = []
        self.inactive_projectiles = []
        for _ in range(projectile_count):
            projectile = Projectile(screen_width, screen_height)
            self.active_projectiles.append(projectile)

    def add_projectiles(self, count):
        for _ in range(count):
            if self.inactive_projectiles:
                projectile = self.inactive_projectiles.pop()
                projectile.reset(
                    self.screen_width, self.screen_height
                )  # Provide screen_width and screen_height
            else:
                projectile = Projectile(self.screen_width, self.screen_height)
            self.active_projectiles.append(projectile)

    def increase_difficulty(self):
        for projectile in self.active_projectiles:
            projectile.speed += 0.1  # Increase speed by a smaller amount
        self.add_projectiles(1)

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

    def reset(self):
        self.active_projectiles.clear()
        self.inactive_projectiles.clear()
        for _ in range(5):
            projectile = Projectile(self.screen_width, self.screen_height)
            self.active_projectiles.append(projectile)
