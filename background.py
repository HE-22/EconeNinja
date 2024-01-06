import pygame


class Background:
    def __init__(self, screen, tile_size=(48, 48)):
        """
        - Initializes the Background class
        - Args:
            - screen: pygame.Surface object where the background will be drawn
            - tile_size: tuple (width, height) defining the size of each tile
        - Returns: None
        """
        self.screen = screen
        self.tile_image = pygame.image.load(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/map/grass_tile.jpg"
        ).convert()
        self.tile_size = tile_size

    def draw(self):
        tile_width, tile_height = self.tile_size
        num_tiles_x = self.screen.get_width() // tile_width
        num_tiles_y = self.screen.get_height() // tile_height

        for y in range(num_tiles_y + 1):  # Add 1 to cover the entire screen
            for x in range(num_tiles_x + 1):
                self.screen.blit(self.tile_image, (x * tile_width, y * tile_height))
