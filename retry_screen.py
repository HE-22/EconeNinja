import pygame
from high_score import get_high_score  # Added this line
from config import (
    DEMON_GAME_OVER_PATH,
)  # Added this line to import the game over sound path from config


class RetryScreen:
    def __init__(
        self, screen, player_score, new_high_score
    ):  # Added new_high_score parameter
        self.screen = screen
        self.font = pygame.font.Font(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/fonts/PixeloidSansBold.ttf",
            36,
        )
        self.text = self.font.render(
            "RIP Bozo!",
            True,
            (255, 0, 0),
        )
        self.text2 = self.font.render(
            "Press R to retry or Q to quit.",
            True,
            (255, 255, 255),
        )
        self.text3 = self.font.render(  # Render "Your score" text in white
            "Your score: ",
            True,
            (255, 255, 255),
        )
        self.text3_score = self.font.render(  # Render player's score in red
            f"{player_score}",
            True,
            (255, 0, 0),
        )
        # Check if player's score is a new high score
        if new_high_score:  # Changed this line to check new_high_score flag
            self.text4 = (
                self.font.render(  # Added this line to render new high score message
                    "New high score!",
                    True,
                    (255, 255, 0),
                )
            )
        else:
            self.text4 = self.font.render(
                "",
                True,
                (0, 0, 0),
            )
        self.textpos3 = self.text3.get_rect(
            centerx=screen.get_width() / 2, centery=screen.get_height() / 2 - 100
        )
        self.textpos4 = self.text4.get_rect(
            centerx=screen.get_width() / 2, centery=screen.get_height() / 2 - 70
        )
        self.textpos = self.text.get_rect(
            centerx=screen.get_width() / 2, centery=screen.get_height() / 2 + 100
        )
        self.textpos2 = self.text2.get_rect(
            centerx=screen.get_width() / 2,
            centery=screen.get_height() / 2 + 250,  # Moved this line further down
        )

        # Load the game over sound effect
        self.game_over_sound = pygame.mixer.Sound(
            DEMON_GAME_OVER_PATH  # Changed this line to use the game over sound path from config
        )

        # Paths to the high score and normal game over music
        self.high_score_music = "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/highscore.ogg"
        self.normal_score_music = "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/game_over_music.ogg"
        self.new_high_score = new_high_score

    def show(self):
        # Stop current music if any
        pygame.mixer.music.stop()

        # Play both sounds
        self.game_over_sound.play()

        # Check if a new high score was achieved and play the appropriate music
        if self.new_high_score:
            pygame.mixer.music.load(self.high_score_music)
        else:
            pygame.mixer.music.load(self.normal_score_music)

        pygame.mixer.music.play()

        # Display retry screen
        retry_screen = pygame.Surface(self.screen.get_size())
        retry_screen.set_alpha(128)  # Make the retry screen transparent
        retry_screen.fill((0, 0, 0))  # Fill the surface with a transparent color
        self.screen.blit(
            retry_screen, (0, 0)
        )  # Blit the transparent surface onto the main screen

        # Blit text directly onto the main screen to keep it fully opaque
        self.screen.blit(self.text3, self.textpos3)
        self.screen.blit(
            self.text3_score,
            (self.textpos3[0] + self.text3.get_width(), self.textpos3[1]),
        )  # Blit player's score next to "Your score" text
        self.screen.blit(self.text4, self.textpos4)
        self.screen.blit(self.text, self.textpos)
        self.screen.blit(self.text2, self.textpos2)

        pygame.display.flip()  # Update the display

        # Wait for player to press R to retry or Q to quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    # self.game_over_sound.stop()
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return False  # Do not retry
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    # self.game_over_sound.stop()
                    pygame.mixer.music.stop()
                    return True  # Retry
