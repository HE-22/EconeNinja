import pygame
import sys
from player import Player
from projectile_shooter import ProjectileShooter
from retry_screen import RetryScreen
from background import Background
from coinspawner import CoinSpawner  # Added this line


def reset_game_state(
    player, projectile_shooter, coin_spawner
):  # Added coin_spawner parameter
    player.reset()
    projectile_shooter.reset()
    coin_spawner.add_coins(1)  # Added this line to spawn a new coin
    pygame.mixer.music.stop()
    pygame.mixer.music.load(
        "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/heroic_demise.mp3"
    )
    pygame.mixer.music.play(loops=-1)


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(
        "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/heroic_demise.mp3"
    )
    pygame.mixer.music.play(loops=-1)

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player = Player()
    projectile_shooter = ProjectileShooter(800, 600, 5)
    background = Background(screen)
    coin_spawner = CoinSpawner(
        800, 600, 0
    )  # Changed this line to spawn no coins initially

    coin_spawner.add_coins(1)  # Added this line to spawn the first coin

    projectile_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(projectile_timer, 2000)
    difficulty_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(
        difficulty_timer, 1000
    )  # Decreased timer interval to increase difficulty faster

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == projectile_timer:
                projectile_shooter.add_projectiles(5)
            elif event.type == difficulty_timer:
                projectile_shooter.increase_difficulty()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()

        player.update_sprite()

        background.draw()
        coin_spawner.draw_coins(screen)  # Added this line
        projectile_shooter.move_projectiles()
        projectile_shooter.draw_projectiles(screen)

        # Handle coin collection
        player.collect_coins(coin_spawner)

        # Handle projectile collisions
        def handle_collision():
            retry_screen = RetryScreen(screen, player.score)
            retry_result = retry_screen.show()
            print(f"Retry result: {retry_result}")
            if not retry_result:
                sys.exit()  # Exit the game if the player does not want to retry
            else:
                reset_game_state(player, projectile_shooter, coin_spawner)

        player.check_projectile_collisions(projectile_shooter, handle_collision)

        player.draw(screen)
        pygame.display.flip()
        clock.tick_busy_loop(60)  # Update game state at a fixed time step


if __name__ == "__main__":
    main()
