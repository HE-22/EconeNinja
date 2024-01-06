import pygame


class Player:
    def __init__(self):
        self.x, self.y = 100, 100
        self.speed = 5
        self.current_sprite = 0
        self.state = "idle"
        self.scale_factor = (60, 60)
        self.load_sprites()
        self.image = self.idle_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.facing_right = False
        self.score = 0  # Added score attribute

    def load_sprites(self):
        def load_sequence(path_format, count):
            return [
                pygame.transform.scale(
                    pygame.image.load(path_format.format(i)), self.scale_factor
                )
                for i in range(count)
            ]

        self.idle_sprites = load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/01-Idle/MN_NINJA_Idle_00{}.png",
            10,
        ) + load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/01-Idle/MN_NINJA_Idle_01{}.png",
            2,
        )
        self.running_sprites = load_sequence(
            "/Users/hassen/local_Dev/GAMES/sample_pygame/assets/sprites/02-Run/MN_NINJA_Run_00{}.png",
            10,
        )

    def update_sprite(self):
        sprite_list = (
            self.idle_sprites if self.state == "idle" else self.running_sprites
        )
        self.current_sprite = (self.current_sprite + 0.1) % len(sprite_list)
        self.image = sprite_list[int(self.current_sprite)]
        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image)  # Update mask position

    def move_right(self):
        self.move(self.speed, 0)
        self.facing_right = True
        self.state = "running"

    def move_left(self):
        self.move(-self.speed, 0)
        self.facing_right = False
        self.state = "running"

    def move_up(self):
        self.move(0, -self.speed)
        self.state = "running"

    def move_down(self):
        self.move(0, self.speed)
        self.state = "running"

    def idle(self):
        self.state = "idle"
        self.update_sprite()

    def check_movement(self):
        keys = pygame.key.get_pressed()
        if not any(
            [
                keys[pygame.K_LEFT],
                keys[pygame.K_RIGHT],
                keys[pygame.K_UP],
                keys[pygame.K_DOWN],
            ]
        ):
            self.idle()

    def reset(self):
        self.x, self.y = 100, 100
        self.speed = 5
        self.current_sprite = 0
        self.state = "idle"
        self.facing_right = False
        self.score = 0  # Reset score
        self.update_sprite()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    # Added collect_coins method
    def collect_coins(self, coin_spawner):
        for coin in coin_spawner.active_coins[:]:
            offset_x = coin.rect.left - self.rect.left
            offset_y = coin.rect.top - self.rect.top
            if self.mask.overlap(coin.mask, (offset_x, offset_y)):
                print("Coin collected!")
                coin_spawner.active_coins.remove(coin)
                self.score += 1
                print(f"Score: {self.score}")
                coin_spawner.add_coins(1)
                coin_spawner.play_coin_sound()  # Play coin collection sound

    # Added check_projectile_collisions method
    def check_projectile_collisions(self, projectile_shooter, on_collision):
        for projectile in projectile_shooter.active_projectiles:
            offset_x = projectile.rect.left - self.rect.left
            offset_y = projectile.rect.top - self.rect.top
            if self.mask.overlap(projectile.mask, (offset_x, offset_y)):
                print("Collision detected!")
                on_collision()  # Callback function to handle collision
