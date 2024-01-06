import pygame
import sys
from player import Player
from projectile_shooter import ProjectileShooter
from retry_screen import RetryScreen
from background import Background
from coinspawner import CoinSpawner  # Added this line
from high_score import update_high_score, get_high_score  # Added get_high_score import
from intro_screen import IntroScreen  # Added this line


def reset_game_state(
    player, projectile_shooter, coin_spawner
):  # Added coin_spawner parameter
    player.reset()
    projectile_shooter.reset()
    coin_spawner.clear_coins()
    coin_spawner.add_coins(1)

    # Added this line to spawn a new coin
    pygame.mixer.music.stop()
    pygame.mixer.music.load(
        "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/hyperloop.mp3"
    )
    pygame.mixer.music.play(loops=-1)


def main():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

    # Create an instance of IntroScreen and run it
    intro_screen = IntroScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    intro_screen.run()

    pygame.mixer.music.load(
        "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/hyperloop.mp3"
    )
    pygame.mixer.music.play(loops=-1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("eConeNinja")  # Set the window title
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    projectile_shooter = ProjectileShooter(SCREEN_WIDTH, SCREEN_HEIGHT, 5)
    background = Background(screen)
    coin_spawner = CoinSpawner(
        SCREEN_WIDTH, SCREEN_HEIGHT
    )  # Changed this line to spawn no coins initially

    coin_spawner.add_coins(1)  # Added this line to spawn the first coin

    projectile_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(projectile_timer, 500)
    difficulty_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(difficulty_timer, 3000)

    death_animation_frame = 0  # Added this line to handle death animation frames

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == projectile_timer:
                projectile_shooter.add_projectiles(3)
            elif event.type == difficulty_timer:
                projectile_shooter.increase_difficulty()

        player.check_movement()

        player.update_sprite()

        background.draw()
        coin_spawner.draw_coins(screen)  # Added this line
        projectile_shooter.move_projectiles()
        projectile_shooter.draw_projectiles(screen)

        # Handle coin collection
        player.collect_coins(coin_spawner)

        # Handle projectile collisions
        def handle_collision():
            nonlocal death_animation_frame  # Access the outer death_animation_frame variable
            death_animation_frame = 0  # Reset the death animation frame counter
            player.play_death_sound()  # Play the death sound

        player.check_projectile_collisions(projectile_shooter, handle_collision)

        # Handle death animation
        if player.is_dead:
            if death_animation_frame < len(player.dead_sprites):
                player.current_sprite = death_animation_frame
                player.update_sprite()
                death_animation_frame += 1
                player.play_death_sound()  # Play the death sound

            else:
                new_high_score = update_high_score(
                    player.score
                )  # Added this line to update high score
                retry_screen = RetryScreen(
                    screen, player.score, new_high_score
                )  # Pass new_high_score flag to RetryScreen
                retry_result = retry_screen.show()
                print(f"Retry result: {retry_result}")
                if not retry_result:
                    sys.exit()  # Exit the game if the player does not want to retry
                else:
                    reset_game_state(player, projectile_shooter, coin_spawner)

        player.draw(screen)
        pygame.display.flip()
        clock.tick_busy_loop(60)  # Update game state at a fixed time step


if __name__ == "__main__":
    main()
