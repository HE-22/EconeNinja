import random


class DifficultyManager:
    def __init__(self):
        self.current_level = 0
        self.time_elapsed = 0

    def update(self, delta_time):
        """
        Updates the difficulty based on the elapsed time.
        """
        self.time_elapsed += delta_time

        # Increase difficulty every 10 seconds
        if self.time_elapsed >= 5000:
            self.current_level += 1
            self.time_elapsed = 0

    def get_difficulty_factor(self):
        """
        Returns the current difficulty factor.
        """
        return 1 + self.current_level * 0.1

    def get_projectile_speed(self):
        """
        - Returns the current average speed of the projectiles.
        - The speed is capped at 10.
        """
        speed = random.randint(1, 6) * self.get_difficulty_factor()
        return min(speed, 10)

    def get_projectile_count(self):
        """
        Returns the current amount of projectiles.
        """
        return 5 + self.current_level

    def get_direction_change_speed(self):
        """
        Returns the current speed at which to change the direction of the projectiles.
        """
        return (
            10000 / self.get_difficulty_factor()
        )  # Change direction more frequently as difficulty increases

    def reset(self):
        """
        Resets the difficulty level and time elapsed.
        """
        self.current_level = 0
        self.time_elapsed = 0

    def __str__(self):
        """
        Returns a string representation of the DifficultyManager.
        """
        return (
            f"Current difficulty: {self.get_difficulty_factor()}\n"
            f"Current average speed of projectiles: {self.get_projectile_speed()}\n"
            f"Current amount of projectiles: {self.get_projectile_count()}\n"
            f"Current speed at which to change the direction of projectiles: {self.get_direction_change_speed()}"
        )
