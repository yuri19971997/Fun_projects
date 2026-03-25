"""Game constants -- all tunable values in one place."""

# Display
MIN_WIDTH = 80
MIN_HEIGHT = 24
FPS = 20  # asciimatics default is ~20fps

# Player
PLAYER_SPEED = 3          # cells per frame when moving (was 2)
PLAYER_START_LIVES = 3
EXTRA_LIFE_SCORE = 5000   # bonus life every N points
BULLET_SPEED = 2
BULLET_COOLDOWN = 2       # frames between shots (was 3, faster fire rate)

# Enemies
CHICKEN_ROWS = 3
CHICKEN_COLS = 8
CHICKEN_H_SPEED = 1  # horizontal movement per step
CHICKEN_V_STEP = 1   # how far down when hitting wall
CHICKEN_MOVE_INTERVAL = 8  # frames between moves (lower = faster)
CHICKEN_SHOOT_CHANCE = 0.003  # probability per chicken per frame (~1 egg/sec total)
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

# Colors (256-palette indices for richer colors)
COLOR_PLAYER = 46       # bright green
COLOR_BULLET = 226      # bright yellow
COLOR_CHICKEN = 209     # orange-red
COLOR_EGG = 231         # white
COLOR_HUD = 255         # bright white
COLOR_SCORE = 226       # yellow
COLOR_COMBO = 196       # red
COLOR_POWERUP = 51      # cyan
COLOR_BOSS = 196        # bright red
COLOR_EXPLOSION = 208   # orange
COLOR_TITLE = 226       # yellow
