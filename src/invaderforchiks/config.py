"""Game constants -- all tunable values in one place."""

# Display
MIN_WIDTH = 80
MIN_HEIGHT = 24
FPS = 20  # asciimatics default is ~20fps

# Player
PLAYER_SPEED = 2          # max cells per frame (40 cells/sec at 20fps)
PLAYER_ACCEL = 2          # = SPEED: instant start/stop, no ramp delay
PLAYER_START_LIVES = 3
EXTRA_LIFE_SCORE = 5000   # bonus life every N points
BULLET_SPEED = 2
BULLET_COOLDOWN = 2       # frames between shots

# Enemies
CHICKEN_ROWS = 3
CHICKEN_COLS = 8
CHICKEN_H_SPEED = 1  # horizontal movement per step
CHICKEN_V_STEP = 1   # how far down when hitting wall
CHICKEN_MOVE_INTERVAL = 4  # frames between moves (was 8, now 2x faster)
CHICKEN_SHOOT_CHANCE = 0.008  # probability per chicken per frame (was 0.003, ~4 eggs/sec)
EGG_SPEED = 1

# Scoring
CHICKEN_POINTS = 10
COMBO_WINDOW = 30  # frames to chain kills
COMBO_MULTIPLIER_CAP = 8

# Waves
TOTAL_WAVES = 20
BOSS_EVERY = 5  # boss on waves 5, 10, 15, 20
SPEED_INCREASE_PER_WAVE = 0.05  # 5% faster each wave

# Power-ups
POWERUP_DROP_CHANCE = 0.15  # chance a killed chicken drops something
POWERUP_FALL_SPEED = 1
POWERUP_TYPES = ["weapon_up", "extra_life", "shield", "missile"]

# Weapon levels
WEAPON_NAMES = ["Pea Shooter", "Dual Shot", "Spread Shot", "Rapid Fire", "Laser Beam", "Homing Eggs"]
WEAPON_MAX_LEVEL = len(WEAPON_NAMES) - 1

# Color mapping for terminals with < 256 colors (e.g. Windows console)
def _map_colour_to_basic(c):
    """Map a 256-color palette index to base 8-color (0-7).

    Used automatically when the terminal doesn't support 256 colors.
    """
    if 0 <= c <= 7:
        return c
    if 8 <= c <= 15:
        return c - 8
    if c >= 232:
        # Grayscale ramp -> white (visible on dark backgrounds)
        return 7
    # 6x6x6 color cube (indices 16-231)
    idx = c - 16
    b = idx % 6
    g = (idx // 6) % 6
    r = idx // 36
    threshold = 3
    is_r, is_g, is_b = r >= threshold, g >= threshold, b >= threshold
    if is_r and is_g and is_b:
        return 7  # white
    if is_r and is_g:
        return 3  # yellow
    if is_r and is_b:
        return 5  # magenta
    if is_g and is_b:
        return 6  # cyan
    if is_r:
        return 1  # red
    if is_g:
        return 2  # green
    if is_b:
        return 4  # blue
    return 7  # default: white (visible on black)


# Colors (256-palette indices for richer colors)
COLOR_PLAYER = 46       # bright green
COLOR_BULLET = 226      # bright yellow
COLOR_CHICKEN = 209     # orange-red
COLOR_EGG = 231         # white
COLOR_HUD = 255         # bright white
COLOR_SCORE = 226       # yellow
COLOR_COMBO = 196       # red
COLOR_POWERUP = 51      # cyan (fallback)
COLOR_POWERUP_WEAPON = 214  # orange -- weapon upgrade
COLOR_POWERUP_LIFE = 46     # green -- extra life
COLOR_POWERUP_SHIELD = 51   # cyan -- shield
COLOR_POWERUP_MISSILE = 196 # red -- missile strike
COLOR_BOSS = 196        # bright red
COLOR_EXPLOSION = 208   # orange
COLOR_TITLE = 226       # yellow
