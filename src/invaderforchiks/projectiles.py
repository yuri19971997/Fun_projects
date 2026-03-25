"""Projectiles -- player bullets, enemy eggs, explosions."""

from . import config, sprites


class Bullet:
    """Player projectile moving upward."""

    def __init__(self, x, y, dx=0, dy=-1, char="|"):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.char = char
        self.alive = True
        self.width = 1
        self.height = 1

    def tick(self):
        self.x += self.dx
        self.y += self.dy
        if self.y < 0 or self.y > 999 or self.x < 0 or self.x > 999:
            self.alive = False

    def render(self, screen):
        if self.alive:
            screen.print_at(self.char, self.x, self.y, colour=config.COLOR_BULLET)


class Egg:
    """Enemy projectile moving downward."""

    def __init__(self, x, y, dy=1):
        self.x = x
        self.y = y
        self.dy = dy
        self.alive = True
        self.width = 1
        self.height = 1

    def tick(self, screen_height):
        self.y += self.dy
        if self.y >= screen_height:
            self.alive = False

    def render(self, screen):
        if self.alive:
            screen.print_at(sprites.EGG, self.x, self.y, colour=config.COLOR_EGG)


class Explosion:
    """Visual-only explosion animation at a position."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.alive = True
        self.total_frames = len(sprites.EXPLOSION_FRAMES)
        self.frame_duration = 3  # ticks per animation frame

    def tick(self):
        self.frame += 1
        if self.frame >= self.total_frames * self.frame_duration:
            self.alive = False

    def render(self, screen):
        if not self.alive:
            return
        anim_idx = min(self.frame // self.frame_duration, self.total_frames - 1)
        art = sprites.EXPLOSION_FRAMES[anim_idx]
        for i, line in enumerate(art):
            screen.print_at(line, self.x - 2, self.y - 1 + i, colour=config.COLOR_EXPLOSION)


class PowerUp:
    """Collectible drop from killed chickens."""

    def __init__(self, x, y, ptype="weapon_up"):
        self.x = x
        self.y = y
        self.ptype = ptype
        self.alive = True
        self.height = 1

    @property
    def char(self):
        if self.ptype == "weapon_up":
            return sprites.POWERUP_WEAPON
        elif self.ptype == "extra_life":
            return sprites.POWERUP_LIFE
        elif self.ptype == "shield":
            return sprites.POWERUP_SHIELD
        elif self.ptype == "missile":
            return sprites.POWERUP_MISSILE
        return "[?]"

    @property
    def width(self):
        return len(self.char)

    @property
    def color(self):
        if self.ptype == "weapon_up":
            return config.COLOR_POWERUP_WEAPON
        elif self.ptype == "extra_life":
            return config.COLOR_POWERUP_LIFE
        elif self.ptype == "shield":
            return config.COLOR_POWERUP_SHIELD
        elif self.ptype == "missile":
            return config.COLOR_POWERUP_MISSILE
        return config.COLOR_POWERUP

    def tick(self, screen_height):
        self.y += config.POWERUP_FALL_SPEED
        if self.y >= screen_height:
            self.alive = False

    def render(self, screen):
        if self.alive:
            from asciimatics.screen import Screen
            screen.print_at(self.char, self.x, self.y, colour=self.color, attr=Screen.A_BOLD)
