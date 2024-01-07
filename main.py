import logging
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
from difficulty_manager import DifficultyManager
from debug_overlay import DebugOverlay
from scoreboard import Scoreboard
from pause_screen import PauseScreen

from config import (
    HYPERLOOP_AUDIO_PATH,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CLOCK_TICK_RATE,
    PROJECTILE_TIMER_INTERVAL,
    DIFFICULTY_TIMER_INTERVAL,
    GAME_TITLE,
    DEBUG_MODE,
)


def reset_game_state(player, projectile_shooter, coin_spawner, difficulty_manager):
    print(
        f"Before reset: player={player}, projectile_shooter={projectile_shooter}, difficulty_manager={difficulty_manager}"
    )
    player.reset()
    projectile_shooter.reset()
    coin_spawner.reset()
    difficulty_manager.reset()

    # Call update_projectiles after difficulty_manager.reset
    projectile_shooter.update_projectiles()
    print(
        f"After reset: player={player}, projectile_shooter={projectile_shooter}, difficulty_manager={difficulty_manager}"
    )

    pygame.mixer.music.stop()
    pygame.mixer.music.load(HYPERLOOP_AUDIO_PATH)
    pygame.mixer.music.play(loops=-1)


def main():
    global DEBUG_MODE
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()  # Add this line

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    is_paused = False
    paused_time = PauseScreen(screen)
    pygame.display.set_caption(GAME_TITLE)

    debug_overlay = DebugOverlay()

    SHOW_START_SCREEN = not DEBUG_MODE

    difficulty_manager = DifficultyManager()

    if SHOW_START_SCREEN:
        start_screen = StartScreen()
        start_screen.run()

    pygame.mixer.music.load(HYPERLOOP_AUDIO_PATH)
    pygame.mixer.music.play(loops=-1)

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    player.invincible = DEBUG_MODE

    projectile_shooter = ProjectileShooter(
        SCREEN_WIDTH, SCREEN_HEIGHT, difficulty_manager
    )
    background = Background(screen)
    coin_spawner = CoinSpawner()

    scoreboard = Scoreboard(10)

    projectile_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(
        projectile_timer, int(difficulty_manager.get_direction_change_speed())
    )  # Change direction every 5 seconds
    difficulty_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(
        difficulty_timer, DIFFICULTY_TIMER_INTERVAL
    )  # Increase difficulty every 30 seconds

    death_animation_frame = 0

    last_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        difficulty_manager.update(delta_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == projectile_timer:
                logging.debug("Projectile timer event")
                projectile_shooter.set_direction(random.uniform(0, 2 * math.pi))
            elif event.type == difficulty_timer:
                print(difficulty_manager)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.dash()
                elif event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
                    logging.debug(f"Escape key pressed, is_paused is now {is_paused}")
                    if is_paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_d:
                    DEBUG_MODE = not DEBUG_MODE
                    player.invincible = DEBUG_MODE
                elif DEBUG_MODE and event.key == pygame.K_r:
                    reset_game_state(
                        player, projectile_shooter, coin_spawner, difficulty_manager
                    )

        if is_paused:
            paused_time.draw()
            pygame.display.flip()
            continue  # Skip the rest of the loop when the game is paused

        background.draw()  # Ensure background is drawn first in the game loop

        player.check_movement()
        if not player.is_hurt:
            player.update_sprite()

        coin_spawner.draw_coins(screen)

        projectile_shooter.update(screen)

        player.collect_coins(coin_spawner)

        def handle_collision():
            player.health -= 1
            if player.health <= 0:  # If player's health is 0 or less
                nonlocal death_animation_frame
                death_animation_frame = 0
                player.is_dead = True
            else:  # If player's health is greater than 0
                player.is_hurt = True  # Set is_hurt to True to play the hurt animation
                print("Handle collision: Player is hurt")  # Debug print statement

        player.check_projectile_collisions(projectile_shooter, handle_collision)
        # print(f"Player is hurt: {player.is_hurt}")  # Debug print statement

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
                    reset_game_state(
                        player, projectile_shooter, coin_spawner, difficulty_manager
                    )

        player.draw(screen)

        scoreboard.update_score(player.score)
        scoreboard.update_hearts(player.health)
        scoreboard.draw(screen)

        # Draw debug overlay
        if DEBUG_MODE:
            # debug_overlay.add_value("Player X", player.x)
            # debug_overlay.add_value("Player Y", player.y)
            # debug_overlay.add_value("Score", player.score)
            debug_overlay.add_value(
                "Difficulty", difficulty_manager.get_difficulty_factor()
            )
            debug_overlay.add_value(
                "Projectile speed", difficulty_manager.get_projectile_speed()
            )
            debug_overlay.add_value(
                "Projectile count", difficulty_manager.get_projectile_count()
            )
            debug_overlay.add_value(
                "Direction change speed",
                difficulty_manager.get_direction_change_speed(),
            )

            debug_overlay.draw(screen)

        pygame.display.flip()
        clock.tick_busy_loop(CLOCK_TICK_RATE)


if __name__ == "__main__":
    main()
