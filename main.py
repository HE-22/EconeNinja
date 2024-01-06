import pygame
import sys
import math
import random
from player import Player
from projectile_shooter import ProjectileShooter
from retry_screen import RetryScreen
from background import Background
from coinspawner import CoinSpawner
from high_score import update_high_score, get_high_score
from start_screen import StartScreen

SHOW_START_SCREEN = True


def reset_game_state(player, projectile_shooter, coin_spawner):
    player.reset()
    projectile_shooter.reset()
    coin_spawner.reset()

    pygame.mixer.music.stop()
    pygame.mixer.music.load(
        "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/hyperloop.mp3"
    )
    pygame.mixer.music.play(loops=-1)


def main():
    pygame.init()
    pygame.mixer.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

    if SHOW_START_SCREEN:
        start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        start_screen.run()

    pygame.mixer.music.load(
        "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/music/hyperloop.mp3"
    )
    pygame.mixer.music.play(loops=-1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("EConeNinja")
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    projectile_shooter = ProjectileShooter(SCREEN_WIDTH, SCREEN_HEIGHT, 5)
    background = Background(screen)
    coin_spawner = CoinSpawner(SCREEN_WIDTH, SCREEN_HEIGHT)

    projectile_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(projectile_timer, 5000)  # Change direction every 5 seconds
    difficulty_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(difficulty_timer, 3000)

    death_animation_frame = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == projectile_timer:
                projectile_shooter.set_direction(random.uniform(0, 2 * math.pi))

        player.check_movement()
        player.update_sprite()

        background.draw()
        coin_spawner.draw_coins(screen)

        projectile_shooter.update(screen)

        player.collect_coins(coin_spawner)

        def handle_collision():
            nonlocal death_animation_frame
            death_animation_frame = 0

        player.check_projectile_collisions(projectile_shooter, handle_collision)

        if player.is_dead:
            if death_animation_frame < len(player.dead_sprites):
                player.current_sprite = death_animation_frame
                player.update_sprite()
                death_animation_frame += 1

            else:
                player.draw(screen)
                new_high_score = update_high_score(player.score)
                retry_screen = RetryScreen(screen, player.score, new_high_score)
                retry_result = retry_screen.show()
                print(f"Retry result: {retry_result}")
                if not retry_result:
                    sys.exit()
                else:
                    reset_game_state(player, projectile_shooter, coin_spawner)

        player.draw(screen)
        pygame.display.flip()
        clock.tick_busy_loop(60)


if __name__ == "__main__":
    main()
