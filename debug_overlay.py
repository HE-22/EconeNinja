import pygame


class DebugOverlay:
    def __init__(self, font_size=20):
        self.font = pygame.font.SysFont("Sans", font_size)  # Changed font to Sans Serif
        self.values = {}

    def add_value(self, name, value):
        self.values[name] = value

    def draw(self, screen):
        for i, (name, value) in enumerate(self.values.items()):
            title = self.font.render(
                f"{name}:", True, (255, 255, 255)
            )  # White color for title
            val = self.font.render(f"{value}", True, (255, 0, 0))  # Red color for value
            screen.blit(title, (10, 10 + i * 20))
            screen.blit(val, (10 + title.get_width(), 10 + i * 20))
