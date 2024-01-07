import logging
import pygame
import math
import yaml


# Load configuration from config.yaml
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)


HIT_SOUND_PATH_1 = config["hit_sound_1_path"]
NORMALIZE_PLAYER_MOVEMENT_FLAG = config["normalize_player_movement_flag"]


class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x, self.y = (
            165,  # Default spawn point x-coordinate
            290,  # Default spawn point y-coordinate
        )
        self.speed = config["player_speed"]
        self.current_sprite = 0
        self.state = "idle"
        self.scale_factor = (60, 60)
        self.load_sprites()
        self.image = self.idle_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.facing_right = False
        self.score = 0  # Added score attribute
        self.is_dead = False
        self.is_hurt = False
        self.invincible = False  # Added invincible attribute
        self.health = 3  # Added health attribute
        self.death_sound = pygame.mixer.Sound(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/audio/sfx/bruh.mp3"
        )  # Load death sound
        self.hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH_1)  # Load hit sound
        self.hurt_animation = (
            self.play_hurt_animation()
        )  # Added hurt_animation attribute

    def normalize_movement(self, dx, dy):
        """
        - Normalize the movement vector and scale by player's speed.
        - Args: dx (int): x component of the movement, dy (int): y component of the movement
        - Returns: (float, float): normalized movement vector scaled by speed
        """
        if (
            not NORMALIZE_PLAYER_MOVEMENT_FLAG
        ):  # Check if normalize_movement flag is False
            return dx, dy
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:  # Avoid division by zero
            return 0, 0
        return dx / length * self.speed, dy / length * self.speed

    def load_sequence(self, path_format, count):
        """
        - Load a sequence of sprites.
        - Args: path_format (str): path format for the sprites, count (int): number of sprites
        - Returns: list: list of loaded and scaled sprites
        """
        return [
            pygame.transform.scale(
                pygame.image.load(path_format.format(i)), self.scale_factor
            )
            for i in range(count)
        ]

    def load_sprites(self):
        self.idle_sprites = self.load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/01-Idle/MN_NINJA_Idle_00{}.png",
            10,
        ) + self.load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/01-Idle/MN_NINJA_Idle_01{}.png",
            2,
        )
        self.running_sprites = self.load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/02-Run/MN_NINJA_Run_00{}.png",
            10,
        )
        self.dead_sprites = self.load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/06-Dead/MN_NINJA_Dead_00{}.png",
            8,
        )
        self.hurt_sprites = self.load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/05-Hurt/MN_NINJA_Hurt_00{}.png",
            6,
        )  # Load hurt animation sprites

    def update_sprite(self):
        """
        - Update the player's sprite based on the current state.
        """
        if self.is_dead:  # If player is dead, play death animation
            sprite_list = self.dead_sprites if self.health <= 0 else self.hurt_sprites
        elif self.is_hurt:  # If player is hurt, play hurt animation
            sprite_list = next(self.hurt_animation)
        else:
            sprite_list = (
                self.idle_sprites if self.state == "idle" else self.running_sprites
            )

        self.current_sprite = (self.current_sprite + 0.1) % len(sprite_list)
        self.image = sprite_list[int(self.current_sprite)]
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

    def is_in_bounds(self, dx, dy):
        """
        - Check if the player is within the screen bounds after the proposed move.
        - Args: dx (int): proposed change in x position, dy (int): proposed change in y position
        - Returns: bool: True if the move keeps the player within bounds, False otherwise
        """
        proposed_x = self.x + dx
        proposed_y = self.y + dy
        return (
            0 <= proposed_x <= self.screen_width
            and 0 <= proposed_y <= self.screen_height
        )

    def move(self, dx, dy):
        """
        - Move the player by dx and dy if the move is within bounds.
        - Args: dx (int): change in x position, dy (int): change in y position
        """
        if self.is_in_bounds(dx, dy):
            # print(f"Moving from ({self.x}, {self.y})")  # Debugging print statement
            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x, self.y)
            self.mask = pygame.mask.from_surface(self.image)  # Update mask position
            # print(f"Moved to ({self.x}, {self.y})")  # Debugging print statement

    def move_right(self):
        dx, dy = self.normalize_movement(self.speed, 0)
        self.move(dx, dy)
        self.facing_right = True
        self.state = "running"

    def move_left(self):
        dx, dy = self.normalize_movement(-self.speed, 0)
        self.move(dx, dy)
        self.facing_right = False
        self.state = "running"

    def move_up(self):
        dx, dy = self.normalize_movement(0, -self.speed)
        self.move(dx, dy)
        self.state = "running"

    def move_down(self):
        dx, dy = self.normalize_movement(0, self.speed)
        self.move(dx, dy)
        self.state = "running"

    def idle(self):
        self.state = "idle"
        self.update_sprite()

    def check_movement(self):
        keys = pygame.key.get_pressed()
        moving = False  # Flag to check if the player is moving

        if keys[pygame.K_LEFT]:
            self.move_left()
            moving = True
        if keys[pygame.K_RIGHT]:
            self.move_right()
            moving = True
        if keys[pygame.K_UP]:
            self.move_up()
            moving = True
        if keys[pygame.K_DOWN]:
            self.move_down()
            moving = True

        if not moving:  # If none of the movement keys are pressed
            self.idle()  # Set the player state to 'idle'

    def reset(self):
        self.x, self.y = (
            165,  # Default spawn point x-coordinate
            290,  # Default spawn point y-coordinate
        )  # Reset player position to the middle of the screen
        # print(f"Reset to ({self.x}, {self.y})")  # Debugging print statement
        self.rect.topleft = (self.x, self.y)  # Update the rect attribute
        self.speed = config["player_speed"]
        self.current_sprite = 0
        self.state = "idle"
        self.facing_right = True
        self.score = 0  # Reset score
        self.is_dead = False  # Reset is_dead
        self.health = 3  # Reset health
        self.update_sprite()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    # Added collect_coins method
    def collect_coins(self, coin_spawner):
        for coin in coin_spawner.active_coins[:]:
            offset_x = coin.rect.left - self.rect.left
            offset_y = coin.rect.top - self.rect.top
            if self.mask.overlap(coin.mask, (offset_x, offset_y)):
                # print("Coin collected!")
                coin_spawner.active_coins.remove(coin)
                self.score += 1
                # print(f"Score: {self.score}")
                coin_spawner.add_coins(1)
                coin_spawner.play_coin_sound()  # Play coin collection sound

    # Added check_projectile_collisions method
    def check_projectile_collisions(self, projectile_shooter, on_collision):
        """
        - Checks for collisions between the player and projectiles.
        - If a collision is detected, calls the on_collision callback function to handle the collision.
        - Args:
            - projectile_shooter: The ProjectileShooter instance.
            - on_collision: Callback function to handle collision.
        """
        if self.invincible:
            return  # Skip collision detection when the player is invincible

        for projectile in projectile_shooter.active_projectiles:
            offset_x = projectile.rect.left - self.rect.left
            offset_y = projectile.rect.top - self.rect.top
            if self.mask.overlap(projectile.mask, (offset_x, offset_y)):
                logging.info("Collision detected!")
                projectile_shooter.active_projectiles.remove(
                    projectile
                )  # Remove the projectile that collided
                self.hit_sound.play()  # Play hit sound
                self.is_hurt = True  # Set is_hurt to True
                self.update_sprite()  # Update sprite to play hurt animation
                self.is_hurt = False  # Set is_hurt back to False
                on_collision()  # Callback function to handle collision

    def play_death_sound(self):
        """
        - Plays the death sound.
        """
        self.death_sound.play()  # Play death sound

    # Added play_death_animation method
    def play_death_animation(self):
        self.state = "dead"
        for i in range(len(self.dead_sprites)):  # Loop through death animation frames
            self.current_sprite = i
            self.update_sprite()

    # Added play_hurt_animation method
    def play_hurt_animation(self):
        """
        - Generator function to play the hurt animation.
        """
        for _ in range(10):  # Play hurt animation for 10 frames
            yield self.hurt_sprites
        while True:  # After hurt animation, yield idle or running sprites
            yield self.idle_sprites if self.state == "idle" else self.running_sprites
