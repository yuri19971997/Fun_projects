"""Player ship -- movement, shooting, rendering."""

from asciimatics.screen import Screen

from . import config, sprites

# Frames to maintain target direction after last keypress.
# Covers the gap between releasing one key and terminal key-repeat starting
# for the new key (~250-500ms).  8 frames @ 20fps = 400ms.
INPUT_WINDOW = 8


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
        self.shield_timer = 0      # frames of shield power-up (separate from hit invincibility)
        self.screen_width = screen_width
        # Smooth acceleration-based movement
        self.vx = 0           # current velocity (smoothly ramps)
        self.target_vx = 0    # desired velocity (set by input)
        self.input_timer = 0  # frames since last direction key

    @property
    def is_shielded(self):
        return self.shield_timer > 0

    def press_direction(self, direction):
        """Called on each direction keypress. Sets target velocity."""
        self.target_vx = direction * config.PLAYER_SPEED
        self.input_timer = INPUT_WINDOW

    def stop(self):
        """Immediately stop moving."""
        self.vx = 0
        self.target_vx = 0
        self.input_timer = 0

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
        if self.invincible_timer > 0 or self.shield_timer > 0:
            if self.shield_timer > 0:
                self.shield_timer = 0  # shield absorbs one hit then breaks
            return False
        self.lives -= 1
        self.invincible_timer = 40  # ~2 seconds of invincibility
        return self.lives <= 0

    def upgrade_weapon(self):
        if self.weapon_level < config.WEAPON_MAX_LEVEL:
            self.weapon_level += 1

    def tick(self):
        """Per-frame update."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.shield_timer > 0:
            self.shield_timer -= 1
        # Input timeout: no keys recently -> target velocity decays to zero
        if self.input_timer > 0:
            self.input_timer -= 1
        else:
            self.target_vx = 0
        # Accelerate toward target velocity (smooth ramp-up and ramp-down)
        if self.vx < self.target_vx:
            self.vx = min(self.vx + config.PLAYER_ACCEL, self.target_vx)
        elif self.vx > self.target_vx:
            self.vx = max(self.vx - config.PLAYER_ACCEL, self.target_vx)
        # Apply velocity
        if self.vx != 0:
            self.x = max(0, min(self.screen_width - self.width, self.x + self.vx))

    def render(self, screen, frame_no):
        # Pick sprite based on state
        if self.shield_timer > 0:
            sprite = sprites.PLAYER_SHIELD
            color = config.COLOR_POWERUP_SHIELD
        elif self.invincible_timer > 0 and frame_no % 4 < 2:
            sprite = sprites.PLAYER_HIT
            color = config.COLOR_PLAYER
        else:
            sprite = sprites.PLAYER_SHIP
            color = config.COLOR_PLAYER

        for i, line in enumerate(sprite):
            screen.print_at(
                line,
                self.x,
                self.y + i,
                colour=color,
                attr=Screen.A_BOLD,
            )
