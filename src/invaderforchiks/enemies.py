"""Chicken enemies -- types, formations, movement patterns."""

import random

from asciimatics.screen import Screen

from . import config, sprites


class Chicken:
    """A single chicken enemy."""

    def __init__(self, x, y, chicken_type="regular"):
        self.x = x
        self.y = y
        self.chicken_type = chicken_type
        self.alive = True
        self.hp = 2 if chicken_type == "armored" else 1
        self.width = sprites.CHICKEN_WIDTH
        self.height = sprites.CHICKEN_HEIGHT

    @property
    def sprite(self):
        if self.chicken_type == "armored":
            return sprites.ARMORED_CHICKEN
        elif self.chicken_type == "bomber":
            return sprites.BOMBER_CHICKEN
        elif self.chicken_type == "kamikaze":
            return sprites.KAMIKAZE_CHICKEN
        return sprites.CHICKEN

    @property
    def color(self):
        if self.chicken_type == "armored":
            return 250  # silver/gray
        elif self.chicken_type == "bomber":
            return 196  # red
        elif self.chicken_type == "kamikaze":
            return 201  # magenta
        return config.COLOR_CHICKEN

    @property
    def points(self):
        base = config.CHICKEN_POINTS
        if self.chicken_type == "armored":
            return base * 2
        elif self.chicken_type == "bomber":
            return base * 3
        elif self.chicken_type == "kamikaze":
            return base * 2
        return base

    @property
    def shoot_chance(self):
        if self.chicken_type == "bomber":
            return config.CHICKEN_SHOOT_CHANCE * 3
        return config.CHICKEN_SHOOT_CHANCE

    def hit(self):
        """Take damage. Returns True if killed."""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def render(self, screen):
        if not self.alive:
            return
        for i, line in enumerate(self.sprite):
            screen.print_at(line, self.x, self.y + i, colour=self.color)


class Formation:
    """A grid of chickens that moves together (Space Invaders style)."""

    def __init__(self, wave, screen_width, y_offset=2):
        self.chickens = []
        self.direction = 1  # 1 = right, -1 = left
        self.move_timer = 0
        self.screen_width = screen_width
        self.wave = wave

        # Adjust formation based on wave
        rows = min(config.CHICKEN_ROWS + wave // 5, 6)
        cols = min(config.CHICKEN_COLS, (screen_width - 10) // (sprites.CHICKEN_WIDTH + 1))
        speed_factor = 1.0 + wave * config.SPEED_INCREASE_PER_WAVE
        self.move_interval = max(2, int(config.CHICKEN_MOVE_INTERVAL / speed_factor))

        for row in range(rows):
            for col in range(cols):
                x = 4 + col * (sprites.CHICKEN_WIDTH + 1)
                y = y_offset + row * (sprites.CHICKEN_HEIGHT + 1)
                ctype = self._pick_type(row, wave)
                self.chickens.append(Chicken(x, y, ctype))

    def _pick_type(self, row, wave):
        """Pick chicken type based on row and wave difficulty."""
        if wave < 3:
            return "regular"
        roll = random.random()
        if row == 0 and wave >= 6 and roll < 0.3:
            return "armored"
        if row <= 1 and wave >= 4 and roll < 0.2:
            return "bomber"
        if wave >= 8 and roll < 0.1:
            return "kamikaze"
        return "regular"

    @property
    def alive_chickens(self):
        return [c for c in self.chickens if c.alive]

    @property
    def all_dead(self):
        return len(self.alive_chickens) == 0

    def tick(self, frame_no):
        """Move the formation. Returns list of new egg projectiles."""
        self.move_timer += 1
        eggs = []

        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            alive = self.alive_chickens
            if not alive:
                return eggs

            # Check bounds
            min_x = min(c.x for c in alive)
            max_x = max(c.x + c.width for c in alive)

            if max_x >= self.screen_width - 1 and self.direction == 1:
                self.direction = -1
                for c in alive:
                    c.y += config.CHICKEN_V_STEP
            elif min_x <= 1 and self.direction == -1:
                self.direction = 1
                for c in alive:
                    c.y += config.CHICKEN_V_STEP
            else:
                for c in alive:
                    c.x += config.CHICKEN_H_SPEED * self.direction

        # Random shooting
        for c in self.alive_chickens:
            if random.random() < c.shoot_chance:
                egg_x = c.x + c.width // 2
                egg_y = c.y + c.height
                eggs.append({"x": egg_x, "y": egg_y, "dy": config.EGG_SPEED})

        return eggs

    def render(self, screen):
        for c in self.chickens:
            c.render(screen)
