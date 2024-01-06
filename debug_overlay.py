import pygame


class DebugOverlay:
    def __init__(self, font_size=20):
        self.font = pygame.font.Font(None, font_size)
        self.values = {}

    def add_value(self, name, value):
        self.values[name] = value

    def draw(self, screen):
        for i, (name, value) in enumerate(self.values.items()):
            text = self.font.render(f"{name}: {value}", True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 20))
