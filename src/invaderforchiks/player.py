"""Player ship -- movement, shooting, rendering."""

from asciimatics.screen import Screen

from . import config, sprites


class Player:
    def __init__(self, screen_width, screen_height):
        self.width = sprites.PLAYER_WIDTH
        self.height = sprites.PLAYER_HEIGHT
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 1  # above bottom HUD bar
        self.lives = config.PLAYER_START_LIVES
        self.weapon_level = 0
        self.shoot_cooldown = 0
        self.invincible_timer = 0  # frames of invincibility after hit
        self.screen_width = screen_width
        # Velocity-based movement: ship keeps moving until stopped
        self.vx = 0
        # Auto-fire: ship keeps shooting when enabled
        self.auto_fire = False

    def set_direction(self, direction):
        """Set movement direction: -1=left, 0=stop, 1=right."""
        self.vx = direction * config.PLAYER_SPEED

    def start_firing(self):
        """Enable auto-fire."""
        self.auto_fire = True

    def stop_firing(self):
        """Disable auto-fire."""
        self.auto_fire = False

    def try_shoot(self):
        """Returns list of new bullet positions if cooldown allows, else empty."""
        if self.shoot_cooldown > 0:
            return []
        self.shoot_cooldown = config.BULLET_COOLDOWN

        center_x = self.x + self.width // 2
        top_y = self.y - 1

        if self.weapon_level == 0:
            return [{"x": center_x, "y": top_y, "dx": 0, "dy": -config.BULLET_SPEED, "char": sprites.BULLET}]
        elif self.weapon_level == 1:
            return [
                {"x": center_x - 1, "y": top_y, "dx": 0, "dy": -config.BULLET_SPEED, "char": sprites.BULLET},
                {"x": center_x + 1, "y": top_y, "dx": 0, "dy": -config.BULLET_SPEED, "char": sprites.BULLET},
            ]
        elif self.weapon_level >= 2:
            return [
                {"x": center_x - 1, "y": top_y, "dx": -1, "dy": -config.BULLET_SPEED, "char": sprites.SPREAD_BULLET_L},
                {"x": center_x, "y": top_y, "dx": 0, "dy": -config.BULLET_SPEED, "char": sprites.BULLET},
                {"x": center_x + 1, "y": top_y, "dx": 1, "dy": -config.BULLET_SPEED, "char": sprites.SPREAD_BULLET_R},
            ]
        return []

    def hit(self):
        """Player takes damage. Returns True if dead."""
        if self.invincible_timer > 0:
            return False
        self.lives -= 1
        self.invincible_timer = 40  # ~2 seconds of invincibility
        return self.lives <= 0

    def upgrade_weapon(self):
        if self.weapon_level < config.WEAPON_MAX_LEVEL:
            self.weapon_level += 1

    def tick(self):
        """Per-frame update -- applies velocity and auto-fire."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        # Apply velocity
        if self.vx != 0:
            self.x = max(0, min(self.screen_width - self.width, self.x + self.vx))

    def render(self, screen, frame_no):
        if self.invincible_timer > 0 and frame_no % 4 < 2:
            sprite = sprites.PLAYER_HIT
        else:
            sprite = sprites.PLAYER_SHIP

        for i, line in enumerate(sprite):
            screen.print_at(
                line,
                self.x,
                self.y + i,
                colour=config.COLOR_PLAYER,
                attr=Screen.A_BOLD,
            )
