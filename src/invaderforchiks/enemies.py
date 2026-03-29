"""Chicken enemies -- types, formations, movement patterns."""

import math
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
    def rich_sprite(self):
        if self.chicken_type == "armored":
            return sprites.ARMORED_CHICKEN_RICH
        elif self.chicken_type == "bomber":
            return sprites.BOMBER_CHICKEN_RICH
        elif self.chicken_type == "kamikaze":
            return sprites.KAMIKAZE_CHICKEN_RICH
        return sprites.CHICKEN_RICH

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
        for row_idx, (chars, colors) in enumerate(self.rich_sprite):
            for col_idx, (ch, fg) in enumerate(zip(chars, colors)):
                if fg and ch != " ":
                    screen.print_at(ch, self.x + col_idx, self.y + row_idx, colour=fg)


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


# ── Boss ─────────────────────────────────────────────────────────────

class Boss:
    """Boss enemy for waves 5/10/15/20. Duck-types as Formation."""

    _DEFS = {
        5:  {"name": "ROOSTER GENERAL", "hp": 30, "w": sprites.BOSS_ROOSTER_W,
             "h": sprites.BOSS_ROOSTER_H, "sprite": "BOSS_ROOSTER_RICH",
             "speed": 1, "interval": 2, "points": 500},
        10: {"name": "EGG MOTHER", "hp": 50, "w": sprites.BOSS_EGG_MOTHER_W,
             "h": sprites.BOSS_EGG_MOTHER_H, "sprite": "BOSS_EGG_MOTHER_RICH",
             "speed": 1, "interval": 3, "points": 1000},
        15: {"name": "COLONEL CLUCK", "hp": 70, "w": sprites.BOSS_COLONEL_W,
             "h": sprites.BOSS_COLONEL_H, "sprite": "BOSS_COLONEL_RICH",
             "speed": 2, "interval": 2, "points": 2000},
        20: {"name": "SUPREME HEN", "hp": 100, "w": sprites.BOSS_SUPREME_W,
             "h": sprites.BOSS_SUPREME_H, "sprite": "BOSS_SUPREME_RICH",
             "speed": 1, "interval": 1, "points": 5000},
    }

    def __init__(self, wave, screen_width):
        d = self._DEFS[wave]
        self.name = d["name"]
        self.hp = d["hp"]
        self.max_hp = d["hp"]
        self.width = d["w"]
        self.height = d["h"]
        self._rich = getattr(sprites, d["sprite"])
        self.move_speed = d["speed"]
        self.move_interval = d["interval"]
        self.points = d["points"]
        self.wave = wave
        self.alive = True
        self.screen_width = screen_width
        self.x = screen_width // 2 - self.width // 2
        self.y = 3
        self.direction = 1
        self.move_timer = 0
        self.attack_timer = 0
        self.chickens = []  # Formation compat

    # ── Formation interface ──────────────────────────────────────────

    @property
    def all_dead(self):
        return not self.alive

    @property
    def alive_chickens(self):
        return [self] if self.alive else []

    def hit(self):
        """Take 1 damage. Returns True if killed."""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    # ── Movement ─────────────────────────────────────────────────────

    def _move(self):
        self.move_timer += 1
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0

        if self.wave == 20:
            # Supreme Hen: sinusoidal weave
            self.x += self.move_speed * self.direction
            self.y = 3 + int(2 * math.sin(self.attack_timer * 0.05))
        else:
            self.x += self.move_speed * self.direction

        if self.x + self.width >= self.screen_width - 1:
            self.direction = -1
        elif self.x <= 1:
            self.direction = 1

    # ── Attacks (each returns list of egg dicts) ─────────────────────

    def _egg(self, x, dy=1, dx=0):
        return {"x": x, "y": self.y + self.height, "dy": dy, "dx": dx}

    def _attack_rooster(self):
        """3-way spread; enraged: 5-way faster."""
        interval = 20 if self.hp < self.max_hp // 2 else 35
        if self.attack_timer % interval != 0:
            return []
        cx = self.x + self.width // 2
        if self.hp < self.max_hp // 2:
            return [self._egg(cx - 3, dx=-1), self._egg(cx - 1),
                    self._egg(cx), self._egg(cx + 1),
                    self._egg(cx + 3, dx=1)]
        return [self._egg(cx - 2, dx=-1), self._egg(cx), self._egg(cx + 2, dx=1)]

    def _attack_egg_mother(self):
        """Egg cluster bombs; enraged: wider clusters."""
        interval = 25 if self.hp < self.max_hp // 2 else 40
        if self.attack_timer % interval != 0:
            return []
        cx = self.x + self.width // 2
        spread = 3 if self.hp < self.max_hp // 2 else 2
        return [self._egg(cx + i * 2) for i in range(-spread, spread + 1)]

    def _attack_colonel(self):
        """Rapid singles + periodic egg wall."""
        eggs = []
        rapid = 10 if self.hp < self.max_hp // 2 else 18
        if self.attack_timer % rapid == 0:
            cx = self.x + self.width // 2
            eggs.append(self._egg(cx))
        wall = 40 if self.hp < self.max_hp // 2 else 70
        if self.attack_timer % wall == 0:
            for i in range(9):
                eggs.append(self._egg(self.x + i * (self.width // 9)))
        return eggs

    def _attack_supreme(self):
        """Everything: spreads, random rain, aimed bursts."""
        eggs = []
        cx = self.x + self.width // 2
        if self.attack_timer % 25 == 0:
            for i in range(-2, 3):
                eggs.append(self._egg(cx + i * 2, dx=i))
        if self.attack_timer % 50 == 0:
            for _ in range(8):
                rx = random.randint(2, self.screen_width - 3)
                eggs.append(self._egg(rx))
        if self.attack_timer % 35 == 0 and self.hp < self.max_hp // 2:
            for i in range(-3, 4):
                eggs.append(self._egg(cx + i, dy=2))
        return eggs

    # ── Tick (Formation interface) ───────────────────────────────────

    def tick(self, frame_no):
        if not self.alive:
            return []
        self._move()
        self.attack_timer += 1
        if self.wave == 5:
            return self._attack_rooster()
        elif self.wave == 10:
            return self._attack_egg_mother()
        elif self.wave == 15:
            return self._attack_colonel()
        return self._attack_supreme()

    # ── Render ───────────────────────────────────────────────────────

    def render(self, screen):
        if not self.alive:
            return
        for row_idx, (chars, colors) in enumerate(self._rich):
            for col_idx, (ch, fg) in enumerate(zip(chars, colors)):
                if fg and ch != " ":
                    screen.print_at(ch, self.x + col_idx, self.y + row_idx, colour=fg)
        self._render_hp_bar(screen)

    def _render_hp_bar(self, screen):
        bar_w = self.width
        filled = max(0, int(bar_w * self.hp / self.max_hp))
        bar = "\u2588" * filled + "\u2591" * (bar_w - filled)
        bar_y = self.y + self.height
        color = RD if self.hp < self.max_hp // 4 else OG if self.hp < self.max_hp // 2 else GR
        screen.print_at(bar, self.x, bar_y, colour=color)
        name_x = self.x + (self.width - len(self.name)) // 2
        screen.print_at(self.name, max(0, name_x), bar_y + 1,
                        colour=255, attr=Screen.A_BOLD)
