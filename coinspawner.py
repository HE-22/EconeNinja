import pygame
import random
from coin import Coin
from config import (
    MIN_COIN_DISTANCE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    INITIAL_COIN_COUNT,
    COIN_SPAWN_MARGIN,
)


class CoinSpawner:
    def create_coin(self):
        """
        - Creates a new coin with random position within the screen boundaries.
        - Returns: Coin object
        """
        while True:
            # Adjusting the range to respect the margins
            margin = COIN_SPAWN_MARGIN
            rand_x = random.randint(margin, self.screen_width - margin - 1)
            rand_y = random.randint(margin, self.screen_height - margin - 1)

            new_coin = Coin(rand_x, rand_y)

            # Check if the new coin is too close to any of the existing coins
            if all(
                coin.distance_to(new_coin) >= MIN_COIN_DISTANCE
                for coin in self.active_coins
            ):
                return new_coin

    def __init__(
        self,
    ):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.starting_coin_count = INITIAL_COIN_COUNT
        self.active_coins = []  # Initialize as an empty list
        self.active_coins = [
            self.create_coin() for _ in range(self.starting_coin_count)
        ]
        self.coin_sounds = [  # Changed this line
            pygame.mixer.Sound(
                "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/sfx/eating_1.mp3"
            ),
            pygame.mixer.Sound(
                "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/sfx/eating_2.mp3"
            ),
        ]  # Added this line

    def add_coins(self, count):
        for _ in range(count):
            self.active_coins.append(self.create_coin())

    def draw_coins(self, screen: pygame.Surface):
        for coin in self.active_coins:
            coin.draw(screen)

    def play_coin_sound(self):  # Modified this method
        random.choice(self.coin_sounds).play()  # Added this line

    def clear_coins(self):
        """
        - Clears all coins from the game.
        """
        self.active_coins = []

    def reset(self):
        """
        - Resets the coin spawner by clearing all coins and adding new ones.
        - Args: coin_count (int): number of coins to add after reset
        """
        self.clear_coins()
        self.add_coins(self.starting_coin_count)
