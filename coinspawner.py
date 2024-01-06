import pygame
import random
from coin import Coin


class CoinSpawner:
    def __init__(self, screen_width, screen_height, coin_count=5):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active_coins = [
            Coin(self.screen_width, self.screen_height) for _ in range(coin_count)
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
            self.active_coins.append(Coin(self.screen_width, self.screen_height))

    def draw_coins(self, screen: pygame.Surface):
        for coin in self.active_coins:
            coin.draw(screen)

    def play_coin_sound(self):  # Modified this method
        random.choice(self.coin_sounds).play()  # Added this line
