import pygame


class RetryScreen:
    def __init__(self, screen, player_score):  # Added player_score parameter
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render(
            "RIP Bozo + L + Ratio + this guy stinks + Actual ",
            True,
            (255, 0, 0),
        )
        self.text2 = self.font.render(
            "Press R to retry or Q to quit.",
            True,
            (255, 255, 255),
        )
        self.text3 = self.font.render(  # Added this line to render player's score
            f"Your score: {player_score}",
            True,
            (255, 255, 255),
        )
        self.textpos3 = self.text3.get_rect(
            centerx=screen.get_width() / 2, centery=screen.get_height() / 2 - 60
        )
        self.textpos = self.text.get_rect(
            centerx=screen.get_width() / 2, centery=screen.get_height() / 2 - 20
        )
        self.textpos2 = self.text2.get_rect(
            centerx=screen.get_width() / 2, centery=screen.get_height() / 2 + 20
        )

        # Load the game over sound effect
        self.game_over_sound = pygame.mixer.Sound(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/demon_game_over.mp3"
        )

        # Load the main music as a Sound object
        self.game_over_music = pygame.mixer.Sound(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/game_over_music.ogg"
        )

    def show(self):
        # Stop current music if any
        pygame.mixer.music.stop()

        # Play both sounds
        self.game_over_sound.play()
        self.game_over_music.play()

        # Display retry screen
        retry_screen = pygame.Surface(self.screen.get_size())
        retry_screen.fill((0, 0, 0))
        retry_screen.blit(self.text3, self.textpos3)
        retry_screen.blit(self.text, self.textpos)
        retry_screen.blit(self.text2, self.textpos2)
        self.screen.blit(retry_screen, (0, 0))
        pygame.display.flip()

        # Wait for player to press R to retry or Q to quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    self.game_over_sound.stop()
                    self.game_over_music.stop()
                    pygame.quit()
                    return False  # Do not retry
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.game_over_sound.stop()
                    self.game_over_music.stop()
                    return True  # Retry

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.game_over_sound.stop()
                    self.game_over_music.stop()
                    return True  # Retry
